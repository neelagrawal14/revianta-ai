import { forwardRef } from 'react';
import { cn } from '../../utils/cn';

const VARIANTS = {
  primary:
    'bg-gradient-to-b from-[#6d70f4] to-[#5257e0] text-white shadow-[0_1px_0_rgba(255,255,255,0.25)_inset,0_10px_30px_-10px_rgba(91,95,240,0.65)] hover:shadow-[0_1px_0_rgba(255,255,255,0.3)_inset,0_14px_36px_-8px_rgba(91,95,240,0.8)]',
  ghost:
    'glass text-text hover:border-white/25 hover:bg-white/[0.06]',
  subtle:
    'bg-white/[0.04] text-text-dim border border-line hover:text-text hover:bg-white/[0.07]',
};

const SIZES = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-11 px-5 text-sm',
  lg: 'h-13 px-7 text-[15px]',
};

/**
 * GlowButton — the single button primitive for Revianta.
 * Prefer `variant="ghost"` for secondary actions instead of inventing
 * new button styles.
 */
const GlowButton = forwardRef(function GlowButton(
  { as: Tag = 'button', variant = 'primary', size = 'md', className, children, ...props },
  ref
) {
  return (
    <Tag
      ref={ref}
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-full font-medium tracking-tight',
        'transition-all duration-200 ease-out active:scale-[0.98]',
        'disabled:opacity-40 disabled:pointer-events-none',
        VARIANTS[variant],
        SIZES[size],
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  );
});

export default GlowButton;
