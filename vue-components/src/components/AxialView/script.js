import { LookupTable } from '../../utils/Colors';
import { toImageURL } from '../../utils/ImageGenerator';

export default {
  name: 'VeraAxial',
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
    xScale: {
      type: Number,
      default: 2,
    },
    yScale: {
      type: Number,
      default: 3,
    },
    xSizes: {
      type: Array,
      default: () => [],
    },
    ySizes: {
      type: Array,
      default: () => [],
    },
  },
  watch: {
    selectedI(i) {
      this.activeI = i;
    },
    selectedJ(j) {
      this.activeJ = j;
    },
    value() {
      this.resize();
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
    colorMap() {
      return this.lookupTable.update(this.colorPreset, this.colorRange);
    },
    images() {
      // Dependencies
      const array = this.value;
      const lut = this.colorMap;

      // Build computed structure
      const images = [];
      for (let j = 0; j < array.length; j++) {
        const line = array[j];
        const lineImages = [];
        images.push(lineImages);
        for (let i = 0; i < line.length; i++) {
          const cell = line[i];
          const cellWidth = cell.length;
          lineImages.push(toImageURL(lut, cell, cellWidth, 1, this.xScale, 1));
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
      let neededWidth = 50;
      for (let i = 0; i < this.xSizes.length; i++) {
        neededWidth += 2 + this.xSizes[i] * this.xScale;
      }
      let neededHeight = 50;
      for (let i = 0; i < this.ySizes.length; i++) {
        neededHeight += 2 + this.ySizes[i] * this.yScale;
      }
      const scale = Math.min(width / neededWidth, height / neededHeight);
      this.scaleStyle = { scale };
      this.sizeStyle = {
        width: `${neededWidth + 10}px`,
        height: `${neededHeight + 10}px`,
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
