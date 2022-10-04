from typing import Union

import h5py
import numpy as np
import string

H5_ARRAY_TYPE = Union[h5py.Dataset, np.ndarray]


class VeraOutFile:
    def __init__(self, filename):
        # Keep this open for better performance
        self.f = h5py.File(filename, "r")
        self.core = VeraOutCore(self.f)
        self.core._cache_all()

        self.states = []

        self._create_states()

        self.active_state_index = 0

    def close(self):
        self.f.close()

    def _create_states(self):
        state_keys = [key for key in self.f if key.startswith("STATE_")]
        indices = [int(key.split("_")[1]) for key in state_keys]
        self.states = [VeraOutState(self.f, idx) for idx in indices]

    @property
    def active_state(self):
        return self.states[self.active_state_index]

    @property
    def active_state_index(self):
        return self._active_state_index

    @active_state_index.setter
    def active_state_index(self, index):
        if hasattr(self, "_active_state_index"):
            if self._active_state_index == index:
                return
            else:
                # Clear the cache from the active state
                self.active_state._uncache_all()

        self._active_state_index = index
        self.active_state._cache_all()

    def array(self, array_name):
        # Get the array with the name "array_name", either on the active state,
        # or on the core.

        # These are on the core
        arrays_on_core = [
            "pin_volumes",
        ]
        if array_name in arrays_on_core:
            # This one is on the core
            return getattr(self.core, array_name)

        # If not on the core, assume it is on the active states.
        return getattr(self.active_state, array_name)


class LazyHDF5Loader:
    def __init__(self, f, path, dataset_names):
        self._f = f
        self._path = path
        self._dataset_names = dataset_names

        self._uncache_all()

    def _load_dataset(self, name):
        return self._f[f"{self._path}/{name}"]

    def _cache(self, name):
        # Set the attribute to be the loaded numpy array
        if name not in self._dataset_names:
            raise AttributeError(name)

        setattr(self, name, self._load_dataset(name)[:])

    def _uncache(self, name):
        # Set the attribute to be the h5py dataset
        if name not in self._dataset_names:
            raise AttributeError(name)

        setattr(self, name, self._load_dataset(name))

    def _cache_all(self):
        for name in self._dataset_names:
            self._cache(name)

    def _uncache_all(self):
        for name in self._dataset_names:
            self._uncache(name)


class VeraOutCore(LazyHDF5Loader):
    # These are the attributes that will be read from the HDF5 file
    axial_mesh: H5_ARRAY_TYPE = None
    core_map: H5_ARRAY_TYPE = None
    core_sym: H5_ARRAY_TYPE = None
    pin_volumes: H5_ARRAY_TYPE = None

    def __init__(self, f):
        super().__init__(f, "/CORE", list(self.__annotations__))
        self.compute_reduced_core_map()
        self.compute_axial_mesh_pixels()
        self.compute_control_rod_positions()
        self.compute_axial_mesh_means()

    def compute_reduced_core_map(self):
        """Compute the reduced core map based upon the core_sym"""
        sym = self.core_sym[0]
        if sym == 1:
            self.reduced_core_map = self.core_map[:].copy()
            self.reduced_core_map_start_index = 0
        elif sym == 4:
            w, h = self.core_map[:].shape
            start_w = w // 2
            start_h = h // 2
            self.reduced_core_map = self.core_map[start_w:, start_h:]
            self.reduced_core_map_start_index = start_w
        else:
            raise Exception(f"Unhandled symmetry: {sym}")

        num_cols = self.reduced_core_map.shape[1]
        alphabet = [*string.ascii_uppercase]
        self.reduced_core_map_column_labels = list(reversed(alphabet[:num_cols]))

    def compute_axial_mesh_pixels(self):
        """Compute the number of pixels that we will be displaying in
        the axial direction for each length in the axial mesh.
        """
        diff_array = np.diff(self.axial_mesh[:])

        # The min diff will be three pixels high. The rest will be computed based
        # upon the min diff.
        MIN_DIFF_PIXELS_HEIGHT = 3
        pixel_height = np.min(diff_array) / MIN_DIFF_PIXELS_HEIGHT
        pixel_height_array = diff_array / pixel_height
        self.axial_mesh_pixels = np.round(pixel_height_array).astype(np.int64)

    def compute_control_rod_positions(self):
        # Assume they are the same in every volume
        first_volume = self.pin_volumes[:, :, 0, 0]
        self.control_rod_positions = np.where(first_volume == 0)

    def compute_axial_mesh_means(self):
        # Compute the mean between each neighbor
        repeats = [2] * len(self.axial_mesh)
        repeats[0] = 1
        repeats[-1] = 1

        repeated_mesh = np.repeat(self.axial_mesh, repeats)
        reshaped = repeated_mesh.reshape((repeated_mesh.shape[0] // 2, 2))

        self.axial_mesh_means = np.mean(reshaped, axis=1)

    def row_assembly_indices(self, assembly_idx):
        """Get indices of all assemblies in the same row as this assembly"""
        # The core map and reduced core map use 1-based indexing
        row = np.where(self.reduced_core_map == assembly_idx + 1)[0][0]
        ids = self.reduced_core_map[row]
        # Remove any zeros
        ids = ids[ids > 0]
        return ids - 1

    def col_assembly_indices(self, assembly_idx):
        """Get indices of all assemblies in the same column as this assembly"""
        col = np.where(self.reduced_core_map == assembly_idx + 1)[1][0]
        ids = self.reduced_core_map[:, col]
        # Remove any zeros
        ids = ids[ids > 0]
        return ids - 1

    def reduced_core_map_assembly(self, i, j):
        # Get the index of the assembly at reduced core map position i, j
        return int(self.reduced_core_map[j, i] - 1)

    def reduced_core_map_ij(self, assembly_idx):
        j, i = map(int, np.where(self.reduced_core_map == assembly_idx + 1))
        return i, j

    def reduced_core_map_label(self, assembly_idx):
        row_label = self.reduced_core_map_row_label(assembly_idx)
        col_label = self.reduced_core_map_column_label(assembly_idx)
        return f"{col_label}-{row_label}"

    def reduced_core_map_row_label(self, assembly_idx):
        i, j = self.reduced_core_map_ij(assembly_idx)
        start_index = self.reduced_core_map_start_index
        rows = list(range(start_index + 1, len(self.core_map) + 1))
        return str(rows[j])

    def reduced_core_map_column_label(self, assembly_idx):
        i, j = self.reduced_core_map_ij(assembly_idx)
        return self.reduced_core_map_column_labels[i]


class VeraOutState(LazyHDF5Loader):
    # These are the attributes that will be read from the HDF5 file
    crit_boron: H5_ARRAY_TYPE = None
    detector_response: H5_ARRAY_TYPE = None
    exposure: H5_ARRAY_TYPE = None
    keff: H5_ARRAY_TYPE = None
    pin_cladtemps: H5_ARRAY_TYPE = None
    pin_fueltemps: H5_ARRAY_TYPE = None
    pin_moddens: H5_ARRAY_TYPE = None
    pin_modtemps: H5_ARRAY_TYPE = None
    pin_powers: H5_ARRAY_TYPE = None

    def __init__(self, f, idx):
        super().__init__(f, f"/STATE_{idx:04}", list(self.__annotations__))
        self._index = idx
