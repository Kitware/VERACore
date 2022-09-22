import vtkColorMaps from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction/ColorMaps';
import vtkColorTransferFunction from '@kitware/vtk.js/Rendering/Core/ColorTransferFunction';

const CANVAS = document.createElement('canvas');

function toImageURL(width, values, lut, scaling = 4) {
  CANVAS.width = width * scaling;
  CANVAS.height = width * scaling;
  const ctx = CANVAS.getContext('2d');

  ctx.mozImageSmoothingEnabled = false;
  ctx.webkitImageSmoothingEnabled = false;
  ctx.msImageSmoothingEnabled = false;
  ctx.imageSmoothingEnabled = false;

  const imgData = ctx.createImageData(width, width);
  let byteIdx = 0;
  const rgba = [];
  for (let i = 0; i < values.length; i++) {
    lut.getColor(values[i], rgba);
    imgData.data[byteIdx++] = rgba[0] * 255 + 0.5;
    imgData.data[byteIdx++] = rgba[1] * 255 + 0.5;
    imgData.data[byteIdx++] = rgba[2] * 255 + 0.5;
    imgData.data[byteIdx++] = 255;
  }
  ctx.putImageData(imgData, 0, 0);
  ctx.drawImage(
    CANVAS,
    0,
    0,
    width,
    width,
    0,
    0,
    width * scaling,
    width * scaling
  );
  return CANVAS.toDataURL('image/png');
}

export default {
  name: 'VeraCore',
  props: {
    value: {
      type: Array,
      default: () => [[[], [], []], [[], []], [[]]],
    },
    selectedI: {
      type: Number,
      default: -1,
    },
    selectedJ: {
      type: Number,
      default: -1,
    },
    colorPreset: {
      type: String,
      default: 'erdc_rainbow_bright',
    },
    colorRange: {
      type: Array,
      default: () => [0, 1],
    },
    activeStyle: {
      type: Object,
      default: () => ({
        outline: 'solid 1px black',
        zIndex: 10,
      }),
    },
    xLabels: {
      type: Array,
      default: () => ['H', 'G', 'F', 'E', 'D', 'C', 'B', 'A'],
    },
    yLabels: {
      type: Array,
      default: () => ['8', '9', '10', '11', '12', '13', '14', '15'],
    },
    scaling: {
      type: Number,
      default: 2,
    },
  },
  watch: {
    selectedI(i) {
      this.activeI = i + 1;
    },
    selectedJ(j) {
      this.activeJ = j + 1;
    },
    value() {
      this.updateImages();
    },
    colorPreset() {
      this.updateLookupTable();
      this.updateImages();
    },
    colorRange() {
      this.updateLookupTable();
      this.updateImages();
    },
  },
  data() {
    return {
      activeI: -1,
      activeJ: -1,
      images: [],
      sizeStyle: { width: '100px', height: '100px' },
      scaleStyle: { scale: 1 },
      imagesReady: 0,
    };
  },
  computed: {
    coreWidth() {
      return this.value[0].length;
    },
    assemblyWidth() {
      return Math.sqrt(this.value[0][0].length);
    },
  },
  created() {
    this.resizeObserver = new ResizeObserver(() => this.resize());
    this.lookupTable = vtkColorTransferFunction.newInstance();
    this.updateLookupTable();
    this.updateImages();
  },
  mounted() {
    this.resizeObserver.observe(this.$el);
  },
  beforeDestroy() {
    this.resizeObserver.disconnect();
    this.resizeObserver = null;
  },
  methods: {
    resize() {
      const { width, height } = this.$el.getBoundingClientRect();
      const neededSize = (this.coreWidth + 1) * 32;
      const availableSpace = Math.min(width, height);
      const scale = availableSpace / neededSize;
      this.scaleStyle = { scale };
      this.sizeStyle = {
        width: `${neededSize + 10}px`,
        height: `${neededSize + 10}px`,
      };
    },
    hover(i, j) {
      this.activeI = i;
      this.activeJ = j;
    },
    exit() {
      this.activeI = this.selectedI;
      this.activeJ = this.selectedJ;
    },
    toStyle(i, j) {
      const style = { cursor: 'pointer' };
      if (i == this.activeI && j == this.activeJ) {
        Object.assign(style, this.activeStyle);
      }
      return style;
    },
    updateLookupTable() {
      const preset = vtkColorMaps.getPresetByName(this.colorPreset);
      this.lookupTable.applyColorMap(preset);
      this.lookupTable.setMappingRange(this.colorRange[0], this.colorRange[1]);
      this.lookupTable.updateRange();
      this.lookupTable.setNanColor(1, 1, 1, 1);
    },
    toUrl(i, j) {
      return this.images?.[j]?.[i];
    },
    updateImages() {
      console.log('updateImages', this.imagesReady);
      const images = [];
      for (let j = 0; j < this.value.length; j++) {
        const line = this.value[j];
        const lineImages = [];
        images.push(lineImages);
        for (let i = 0; i < line.length; i++) {
          lineImages.push(
            toImageURL(
              this.assemblyWidth,
              line[i],
              this.lookupTable,
              this.scaling
            )
          );
        }
      }
      this.images = images;
      this.imagesReady++;
    },
  },
};
