import { forwardRef } from 'react';
import { cn } from '../../utils/cn';

/**
 * FormField — labeled input used across auth and (later) project forms.
 */
const FormField = forwardRef(function FormField(
  { label, id, type = 'text', trailing, className, ...props },
  ref
) {
  return (
    <div className={className}>
      <label htmlFor={id} className="mb-1.5 block text-sm text-text-dim">
        {label}
      </label>
      <div className="relative">
        <input
          ref={ref}
          id={id}
          type={type}
          className={cn(
            'h-11 w-full rounded-xl border border-line bg-white/[0.03] px-3.5 text-sm text-text placeholder:text-text-faint',
            'transition-colors focus:border-indigo/50 focus:bg-white/[0.05] focus:outline-none',
            trailing && 'pr-10'
          )}
          {...props}
        />
        {trailing && <div className="absolute inset-y-0 right-2 flex items-center">{trailing}</div>}
      </div>
    </div>
  );
});

export default FormField;
