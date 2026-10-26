import { cn } from '../../utils/cn';

/**
 * SectionHeader — title + optional description + optional trailing action.
 * Used at the top of dashboard sections and page bodies (not the landing
 * page, which sets its own section headings for editorial control).
 */
export default function SectionHeader({ title, description, action, className }) {
  return (
    <div className={cn('flex items-end justify-between gap-6', className)}>
      <div>
        <h2 className="font-display text-xl text-text sm:text-2xl">{title}</h2>
        {description && <p className="mt-1.5 max-w-prose text-sm text-text-dim">{description}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
