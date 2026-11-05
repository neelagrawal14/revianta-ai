/**
 * Joins class names, skipping falsy values.
 * Small local replacement for `clsx` to avoid an extra dependency.
 */
export function cn(...classes) {
  return classes.filter(Boolean).join(' ');
}
