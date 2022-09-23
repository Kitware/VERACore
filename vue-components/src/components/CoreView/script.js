import { LookupTable } from '../../utils/Colors';
import { toImageURL } from '../../utils/ImageGenerator';

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
      this.activeI = i;
    },
    selectedJ(j) {
      this.activeJ = j;
    },
  },
  data() {
    return {
      activeI: this.selectedI,
      activeJ: this.selectedJ,
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
    colorMap() {
      return this.lookupTable.update(this.colorPreset, this.colorRange);
    },
    images() {
      // Dependencies
      const array = this.value;
      const lut = this.colorMap;
      const width = this.assemblyWidth;

      // Build computed structure
      const images = [];
      for (let j = 0; j < array.length; j++) {
        const line = array[j];
        const lineImages = [];
        images.push(lineImages);
        for (let i = 0; i < line.length; i++) {
          lineImages.push(
            toImageURL(lut, line[i], width, width, this.scaling, this.scaling)
          );
        }
      }
      this.imagesReady++;
      return images;
    },
  },
  created() {
    this.resizeObserver = new ResizeObserver(() => this.resize());
    this.lookupTable = new LookupTable(this.colorPreset, this.colorRange);
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
    toUrl(i, j) {
      return this.images?.[j]?.[i];
    },
  },
};
