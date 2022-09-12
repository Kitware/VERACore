export default {
  name: 'VeraTopQuadrant',
  props: {
    size: {
      type: Number,
      default: 8,
    },
    xLabels: {
      type: Array,
      default: () => ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    },
    yLabels: {
      type: Array,
      default: () => ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    },
    value: {
      type: Array,
      default: () => [0, 0],
    },
    quadrantValues: {
      type: Array,
    },
    colorPreset: {
      type: String,
      default: '',
    },
    colorRange: {
      type: Array,
      default: () => [0, 1],
    },
  },
  methods: {
    getBlockStyle(i, j) {
      if (i % 2 === 0 && j % 2 === 0) {
        return { background: 'red' };
      }
      return { background: 'green' };
    }
  }
};
