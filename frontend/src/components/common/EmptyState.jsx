import { cn } from '../../utils/cn';
import GlowButton from './GlowButton';

/**
 * EmptyState — treats an empty screen as an invitation to act, per
 * Revianta's voice: direct, unapologetic, tells you the next step.
 */
export default function EmptyState({ icon: Icon, title, description, actionLabel, onAction, className }) {
  return (
    <div className={cn('flex flex-col items-center justify-center gap-4 rounded-[22px] border border-dashed border-line py-16 text-center', className)}>
      {Icon && (
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-white/[0.04] text-text-dim">
          <Icon size={20} />
        </div>
      )}
      <div className="max-w-sm">
        <h3 className="font-display text-lg text-text">{title}</h3>
        {description && <p className="mt-1.5 text-sm text-text-dim">{description}</p>}
      </div>
      {actionLabel && (
        <GlowButton size="sm" onClick={onAction}>
          {actionLabel}
        </GlowButton>
      )}
    </div>
  );
}
