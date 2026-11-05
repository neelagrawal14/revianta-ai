/**
 * Small helpers shared across the Part 2 mock-data generators. These
 * exist purely to keep every project's Papers/GitHub/Datasets/Patents
 * pages populated with plausible-looking (clearly synthetic) content
 * instead of empty states for every project except the flagship demo.
 */

/** Deterministic pseudo-random number in [0, 1) seeded by a string. */
export function seededRandom(seed) {
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = (Math.imul(31, h) + seed.charCodeAt(i)) | 0;
  }
  return () => {
    h = (Math.imul(48271, h) + 12345) | 0;
    return ((h >>> 0) % 100000) / 100000;
  };
}

export function pickOne(rand, arr) {
  return arr[Math.floor(rand() * arr.length)];
}

export function pickN(rand, arr, n) {
  const copy = [...arr];
  const out = [];
  while (out.length < n && copy.length) {
    const idx = Math.floor(rand() * copy.length);
    out.push(copy.splice(idx, 1)[0]);
  }
  return out;
}

export function round(n, decimals = 0) {
  const f = 10 ** decimals;
  return Math.round(n * f) / f;
}
