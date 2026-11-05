/**
 * isWebGLAvailable — cheap feature check so the 3D hero can fall back to
 * the static NodeGraph SVG on browsers/devices without WebGL instead of
 * throwing or rendering a blank canvas.
 */
export function isWebGLAvailable() {
  try {
    const canvas = document.createElement('canvas');
    return Boolean(window.WebGLRenderingContext && (canvas.getContext('webgl2') || canvas.getContext('webgl')));
  } catch {
    return false;
  }
}
