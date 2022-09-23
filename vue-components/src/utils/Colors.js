import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import vtkColorTransferFunction from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction';

export class LookupTable {
  constructor(
    presetName = 'jet',
    colorRange = [0, 1],
    nanColor = [1, 1, 1, 1]
  ) {
    this.lookupTable = vtkColorTransferFunction.newInstance();
    this.lookupTable.setNanColor(...nanColor);
    this.update(presetName, colorRange);
    this.rgba = [0, 0, 0, 0];
  }

  update(presetName, colorRange) {
    const preset = vtkColorMaps.getPresetByName(presetName);
    this.lookupTable.applyColorMap(preset);
    this.lookupTable.setMappingRange(colorRange[0], colorRange[1]);
    this.lookupTable.updateRange();
    return this;
  }

  applyRGBA(value, offset, array) {
    this.lookupTable.getColor(value, this.rgba);
    array[offset] = this.rgba[0] * 255 + 0.5;
    array[offset + 1] = this.rgba[1] * 255 + 0.5;
    array[offset + 2] = this.rgba[2] * 255 + 0.5;
    array[offset + 3] = 255;

    return offset + 4;
  }
}
