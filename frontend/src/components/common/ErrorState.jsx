import { TriangleAlert } from 'lucide-react';
import { cn } from '../../utils/cn';
import GlowButton from './GlowButton';

/**
 * ErrorState — explains what went wrong and how to fix it, in the
 * interface's voice. Never apologetic, never vague.
 */
export default function ErrorState({
  title = 'This didn\u2019t load',
  description = 'The request failed before it reached the research engine. Try again.',
  actionLabel = 'Retry',
  onAction,
  className,
}) {
  return (
    <div
      role="alert"
      className={cn(
        'flex flex-col items-center justify-center gap-4 rounded-[22px] border border-rose/25 bg-rose/[0.04] py-16 text-center',
        className
      )}
    >
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-rose/10 text-rose">
        <TriangleAlert size={20} />
      </div>
      <div className="max-w-sm">
        <h3 className="font-display text-lg text-text">{title}</h3>
        <p className="mt-1.5 text-sm text-text-dim">{description}</p>
      </div>
      {onAction && (
        <GlowButton size="sm" variant="subtle" onClick={onAction}>
          {actionLabel}
        </GlowButton>
      )}
    </div>
  );
}
