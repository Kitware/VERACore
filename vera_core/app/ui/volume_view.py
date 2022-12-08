import copy

import numpy as np

from vtkmodules.vtkCommonDataModel import vtkImageData, vtkPiecewiseFunction
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

import vtk.util.numpy_support as np_s

from trame.ui.html import DivLayout
from trame.widgets import vtk, vuetify

OPTION = {
    "name": "volume_view",
    "label": "Volume View",
    "icon": "mdi-rotate-3d",
}

reset_camera_count = 0


def initialize(server, vera_out_file):
    state, ctrl = server.state, server.controller

    if OPTION not in state.grid_options:
        state.grid_options.append(OPTION)

    # Set up the VTK volume
    ren = vtkRenderer()
    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.OffScreenRenderingOn()

    ren.SetBackground(1, 1, 1)

    iren = vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
    iren.SetRenderWindow(ren_win)

    axes = vtkAxesActor()
    orientation_marker = vtkOrientationMarkerWidget()
    orientation_marker.SetOrientationMarker(axes)
    orientation_marker.SetInteractor(iren)
    # FIXME: I'm not sure if this is accurate, so it is disabled for now
    # orientation_marker.EnabledOn()
    # orientation_marker.InteractiveOn()

    # FIXME: for now, let's make it fully opaque so it matches veraview
    # exactly.
    opacity_points = [
        (0.00, 0),
        (0.01, 1),
        (1.95, 1),
    ]

    # Create transfer mapping scalar value to opacity.
    opacity_transfer_function = vtkPiecewiseFunction()
    for point in opacity_points:
        opacity_transfer_function.AddPoint(*point)

    # This is for a rainbow color map
    original_color_points = [
        (0.000000, 0.0, 0.0, 0.5625),
        (0.216992, 0.0, 0.0, 1.0000),
        (0.712975, 0.0, 1.0, 1.0000),
        (0.960965, 0.5, 1.0, 0.5000),
        (1.208960, 1.0, 1.0, 0.0000),
        (1.704940, 1.0, 0.0, 0.0000),
        (1.952930, 0.5, 0.0, 0.0000),
    ]

    # Create transfer mapping scalar value to color.
    color_transfer_function = vtkColorTransferFunction()
    for point in original_color_points:
        color_transfer_function.AddRGBPoint(*point)

    # The property describes how the data will look.
    volume_property = vtkVolumeProperty()
    volume_property.SetColor(color_transfer_function)
    volume_property.SetScalarOpacity(opacity_transfer_function)
    # I don't think we want to shade the data or perform linear interpolation
    # volume_property.ShadeOn()
    # volume_property.SetInterpolationTypeToLinear()

    volume_data = vtkImageData()
    volume_mapper = vtkSmartVolumeMapper()
    volume_mapper.SetInputData(volume_data)

    volume = vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    ren.AddVolume(volume)

    # Pitch the camera by 90 degrees to start
    ren.GetActiveCamera().Pitch(90)
    ren.GetActiveCamera().OrthogonalizeViewUp()

    @state.change("color_range")
    def update_color_points(color_range, **kwargs):
        # Rescale our color points when the color range changes
        original_range = (original_color_points[0][0], original_color_points[-1][0])
        new_color_points = copy.deepcopy(original_color_points)
        for i, row in enumerate(new_color_points):
            value = row[0]
            new_value = np.interp(value, original_range, color_range)
            new_color_points[i] = (new_value, *row[1:])

        color_transfer_function.RemoveAllPoints()
        for point in new_color_points:
            color_transfer_function.AddRGBPoint(*point)

        ren_win.Render()
        ctrl.view_update()

    @state.change("selected_array")
    @ctrl.add("on_vera_out_active_state_index_changed")
    def update_volume_view(selected_array, **kwargs):
        global reset_camera_count
        array = vera_out_file.array(selected_array)

        # Let's convert the data into a volume format
        assembly_shape = array.shape[:2]
        reduced_core_map = vera_out_file.core.reduced_core_map
        reduced_map_shape = reduced_core_map.shape
        expanded_core_shape = (
            reduced_map_shape[0] * assembly_shape[0],
            reduced_map_shape[1] * assembly_shape[1],
        )
        volume_shape = (*expanded_core_shape, array.shape[2])
        volume_array = np.zeros(volume_shape, dtype=array.dtype)

        # Now that we have the array, let's copy the assemblies into it
        for assembly_id in range(array.shape[3]):
            core_i, core_j = map(int, np.where(reduced_core_map == assembly_id + 1))
            i_range = (core_i * assembly_shape[0], (core_i + 1) * assembly_shape[0])
            j_range = (core_j * assembly_shape[1], (core_j + 1) * assembly_shape[1])

            volume_array[slice(*i_range), slice(*j_range)] = array[:, :, :, assembly_id]

        # It's possible that a rectilinear grid would be better here rather
        # than repeating voxels. But it also doesn't look super straightforward
        # to render a rectilinear grid as a volume. So let's just repeat the
        # voxels instead.
        axial_mesh_pixels = vera_out_file.core.axial_mesh_pixels
        volume_array = np.repeat(volume_array, axial_mesh_pixels, axis=2)

        # Since VTK uses Fortran ordering, we should transpose before raveling.
        raveled = volume_array.transpose(2, 1, 0).ravel()
        vtk_array = np_s.numpy_to_vtk(raveled, deep=True)

        volume_data.SetDimensions(*volume_array.shape)
        pd = volume_data.GetPointData()

        # Remove all other arrays
        while pd.GetNumberOfArrays() > 0:
            pd.RemoveArray(0)

        # Add the array
        pd.SetScalars(vtk_array)
        volume_data.Modified()

        # Update the view
        # ren_win.Render()
        if reset_camera_count < 2:
            ren.ResetCameraClippingRange()
            ren.ResetCamera()
            reset_camera_count += 1
            ctrl.reset_camera()

        ctrl.view_update()

        # Save a copy of the orientation marker so it won't go out of scope
        om = orientation_marker  # noqa

    with DivLayout(server, template_name="volume_view") as layout:
        layout.root.style = "height: 100%;"
        html_view = vtk.VtkRemoteView(ren_win, ref="volume_view")
        ctrl.reset_camera = html_view.reset_camera
        ctrl.view_update = html_view.update

        with vuetify.VBtn(
            icon=True,
            click=html_view.reset_camera,
            absolute=True,
            style="top: 0; right: 2px",
            small=True,
        ):
            vuetify.VIcon("mdi-crop-free", small=True)
