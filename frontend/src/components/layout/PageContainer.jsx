import { cn } from '../../utils/cn';

/**
 * PageContainer — consistent max-width + padding wrapper for content
 * rendered inside the AppShell's main area.
 */
export default function PageContainer({ className, children }) {
  return (
    <div className={cn('mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 lg:py-10', className)}>
      {children}
    </div>
  );
}
