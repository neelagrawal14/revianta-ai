import { ChevronDown } from 'lucide-react';
import { cn } from '../../utils/cn';

/**
 * SelectField — small styled <select>, used for sort/filter controls on
 * the Papers/GitHub/Datasets/Patents/Notes/Experiments list pages so
 * every page shares one control style instead of inventing new ones.
 */
export default function SelectField({ value, onChange, options, label, className }) {
  return (
    <label className={cn('relative flex items-center gap-2 text-sm text-text-dim', className)}>
      {label && <span className="hidden sm:inline">{label}</span>}
      <span className="relative">
        <select
          value={value}
          onChange={onChange}
          className="h-10 appearance-none rounded-full border border-line bg-white/[0.03] py-0 pl-3.5 pr-8 text-sm text-text focus:border-indigo/40 focus:outline-none"
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value} className="bg-surface text-text">
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown size={14} className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-text-faint" />
      </span>
    </label>
  );
}
