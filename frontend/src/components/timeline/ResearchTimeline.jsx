import { motion } from 'framer-motion';
import GlassCard from '../common/GlassCard';
import Badge from '../common/Badge';

/**
 * ResearchTimeline — signature visual #5: a vertical timeline of how the
 * technology landscape around a topic evolved year over year. Shared by
 * the workspace-level /timeline page and each project's Timeline tab.
 */
export default function ResearchTimeline({ entries }) {
  return (
    <div className="relative">
      <div className="absolute bottom-0 left-[27px] top-0 w-px bg-line sm:left-[35px]" aria-hidden="true" />

      <div className="space-y-8">
        {entries.map((entry, i) => (
          <motion.div
            key={entry.year}
            initial={{ opacity: 0, y: 14 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.5, delay: i * 0.05 }}
            className="relative flex gap-5 pl-14 sm:gap-7 sm:pl-20"
          >
            <span className="absolute left-0 flex h-14 w-14 shrink-0 items-center justify-center rounded-full border border-indigo/30 bg-surface font-mono text-sm text-indigo-soft sm:h-[70px] sm:w-[70px]">
              {entry.year}
            </span>

            <GlassCard className="flex-1 p-5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <h3 className="font-display text-base text-text">{entry.technology}</h3>
                <Badge tone="indigo">{entry.shift}</Badge>
              </div>
              <p className="mt-2 text-sm text-text-dim">{entry.description}</p>
              {entry.papers?.length > 0 && (
                <div className="mt-3 flex flex-wrap gap-1.5 border-t border-line pt-3">
                  {entry.papers.map((p) => (
                    <span key={p} className="mono-tag rounded-full border border-line bg-white/[0.03] px-2.5 py-1 text-text-faint">
                      {p}
                    </span>
                  ))}
                </div>
              )}
            </GlassCard>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
