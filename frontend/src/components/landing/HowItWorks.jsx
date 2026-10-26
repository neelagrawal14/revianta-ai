import { motion } from 'framer-motion';
import { MOCK_PIPELINE_STAGES } from '../../constants/mockData';

/**
 * A real sequence (idea → workspace), so numbered markers are earned here.
 */
export default function HowItWorks() {
  return (
    <section id="how-it-works" className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <div className="max-w-xl">
          <h2 className="font-display text-3xl text-text sm:text-4xl">How Revianta works</h2>
          <p className="mt-4 text-text-dim">
            One idea moves through eight stages of analysis before it ever reaches your workspace.
          </p>
        </div>

        <div className="relative mt-14">
          {/* connecting line */}
          <div className="absolute left-[15px] top-0 h-full w-px bg-line lg:left-0 lg:top-[15px] lg:h-px lg:w-full" />

          <div className="grid gap-8 lg:grid-cols-4 lg:gap-6">
            {MOCK_PIPELINE_STAGES.map((stage, i) => (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, y: 12 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.5, delay: (i % 4) * 0.06, ease: [0.19, 1, 0.22, 1] }}
                className="relative flex gap-4 pl-10 lg:flex-col lg:gap-3 lg:pl-0"
              >
                <span className="absolute left-0 top-0 flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-indigo/35 bg-surface font-mono text-xs text-indigo-soft lg:static">
                  {String(i + 1).padStart(2, '0')}
                </span>
                <div>
                  <h3 className="font-display text-[15px] text-text">{stage.label}</h3>
                  <p className="mt-1 text-sm text-text-dim">{stage.hint}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
