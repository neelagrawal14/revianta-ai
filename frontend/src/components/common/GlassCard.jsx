import { cn } from '../../utils/cn';

/**
 * GlassCard — the base translucent surface used across Revianta.
 * Keep usage sparing: not every block of content needs to be a card.
 *
 * @param {'default'|'strong'} tone
 * @param {boolean} interactive - adds hover lift + border glow
 */
export default function GlassCard({
  as: Tag = 'div',
  tone = 'default',
  interactive = false,
  glow,
  className,
  children,
  ...props
}) {
  return (
    <Tag
      className={cn(
        tone === 'strong' ? 'glass-strong' : 'glass',
        'rounded-[22px] relative',
        interactive &&
          'transition-all duration-300 ease-out hover:-translate-y-0.5 hover:border-white/20 focus-visible:-translate-y-0.5',
        glow === 'indigo' && 'shadow-[0_0_0_1px_rgba(91,95,240,0.25),0_0_40px_-12px_rgba(91,95,240,0.5)]',
        glow === 'cyan' && 'shadow-[0_0_0_1px_rgba(53,224,208,0.25),0_0_40px_-12px_rgba(53,224,208,0.45)]',
        className
      )}
      {...props}
    >
      {children}
    </Tag>
  );
}
