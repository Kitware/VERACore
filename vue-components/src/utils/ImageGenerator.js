const CANVAS = document.createElement('canvas');

export function toImageURL(
  lut,
  values,
  width,
  height,
  xScaling = 1,
  yScaling = 1
) {
  CANVAS.width = width * xScaling;
  CANVAS.height = height * yScaling;

  const ctx = CANVAS.getContext('2d');
  ctx.clearRect(0, 0, CANVAS.width, CANVAS.height);

  // Disable interpolation
  ctx.mozImageSmoothingEnabled = false;
  ctx.webkitImageSmoothingEnabled = false;
  ctx.msImageSmoothingEnabled = false;
  ctx.imageSmoothingEnabled = false;

  const imgData = ctx.createImageData(width, height);
  let offset = 0;
  for (let i = 0; i < values.length; i++) {
    offset = lut.applyRGBA(values[i], offset, imgData.data);
  }
  ctx.putImageData(imgData, 0, 0);
  ctx.drawImage(
    CANVAS,
    0,
    0,
    width,
    height,
    0,
    0,
    width * xScaling,
    height * yScaling
  );
  return CANVAS.toDataURL('image/png');
}
