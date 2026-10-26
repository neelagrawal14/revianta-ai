import { FileSearch, Repeat, ShieldOff } from 'lucide-react';
import GlassCard from '../common/GlassCard';

const PROBLEMS = [
  {
    icon: FileSearch,
    title: 'Prior art hides in plain sight',
    body: 'The paper that already solved half your problem is out there — scattered across arXiv, GitHub, and patent filings you\u2019ll never think to search.',
  },
  {
    icon: Repeat,
    title: 'Feasibility is discovered too late',
    body: 'Teams often learn a technical approach won\u2019t scale months into a build, after the architecture is already load-bearing.',
  },
  {
    icon: ShieldOff,
    title: 'Risk stays invisible until it isn\u2019t',
    body: 'Overlapping patents, abandoned approaches, and dead-end technologies rarely surface until they\u2019ve already cost you time.',
  },
];

export default function ProblemSection() {
  return (
    <section className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <div className="max-w-xl">
          <h2 className="font-display text-3xl text-text sm:text-4xl">
            Most research happens after the decision is already made.
          </h2>
          <p className="mt-4 text-text-dim">
            By the time a team validates its own idea, they've usually already committed to
            a direction. Revianta moves that research earlier, where it actually changes outcomes.
          </p>
        </div>

        <div className="mt-12 grid gap-4 sm:grid-cols-3">
          {PROBLEMS.map(({ icon: Icon, title, body }) => (
            <GlassCard key={title} className="p-6">
              <Icon size={20} className="text-indigo-soft" />
              <h3 className="mt-4 font-display text-[17px] text-text">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-text-dim">{body}</p>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>
  );
}
