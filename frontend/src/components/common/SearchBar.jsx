import { Search } from 'lucide-react';
import { cn } from '../../utils/cn';

/**
 * SearchBar — used in the TopBar and inside page bodies (e.g. Projects list).
 * `hint` renders a keyboard-shortcut style label on the right (decorative
 * unless `onHintClick`/global shortcut is wired up later).
 */
export default function SearchBar({
  placeholder = 'Search research, projects, technologies…',
  hint = '⌘K',
  className,
  ...props
}) {
  return (
    <label
      className={cn(
        'group flex h-10 items-center gap-2.5 rounded-full border border-line bg-white/[0.03] px-4',
        'transition-colors focus-within:border-indigo/40 focus-within:bg-white/[0.05]',
        className
      )}
    >
      <Search size={16} className="shrink-0 text-text-faint group-focus-within:text-indigo-soft" />
      <input
        type="text"
        placeholder={placeholder}
        aria-label={placeholder}
        className="w-full bg-transparent text-sm text-text placeholder:text-text-faint focus:outline-none"
        {...props}
      />
      {hint && (
        <kbd className="mono-tag hidden shrink-0 rounded-md border border-line px-1.5 py-0.5 text-text-faint sm:block">
          {hint}
        </kbd>
      )}
    </label>
  );
}
