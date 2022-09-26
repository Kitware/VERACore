import { LookupTable } from '../../utils/Colors';
import { toImageURL } from '../../utils/ImageGenerator';

function simplifyNumber(v, targetSize = 6) {
  let strValue = `${v}`;
  let precision = targetSize;
  while (strValue.length > 6) {
    precision -= 1;
    strValue = v.toFixed(precision);
  }
  return Number(strValue);
}

export default {
  name: 'VeraColorMapEditor',
  props: {
    value: {
      type: Array,
      default: () => [0, 1],
    },
    colorPreset: {
      type: String,
      default: 'erdc_rainbow_bright',
    },
  },
  data() {
    return {
      minValue: simplifyNumber(this.value[0]),
      maxValue: simplifyNumber(this.value[1]),
    };
  },
  watch: {
    value() {
      this.minValue = simplifyNumber(this.value[0]);
      this.maxValue = simplifyNumber(this.value[1]);
    },
  },
  computed: {
    colorMap() {
      return this.lookupTable.update(this.colorPreset, this.value);
    },
    imgSrc() {
      const samples = [];
      const delta = (this.value[1] - this.value[0]) / 512;
      let v = this.value[0];
      while (v < this.value[1]) {
        samples.push(v);
        v += delta;
      }
      return toImageURL(this.colorMap, samples, samples.length, 1);
    },
  },
  created() {
    this.lookupTable = new LookupTable(this.colorPreset, this.value);
  },
  methods: {
    validateRange() {
      let error = 0;
      const v0 = Number(this.minValue);
      if (Number.isNaN(v0)) {
        this.minValue = simplifyNumber(this.value[0]);
        error++;
      }

      const v1 = Number(this.maxValue);
      if (Number.isNaN(v1)) {
        this.maxValue = simplifyNumber(this.value[1]);
        error++;
      }
      if (error === 0) {
        this.$emit('input', [v0, v1]);
      }
    },
  },
};
