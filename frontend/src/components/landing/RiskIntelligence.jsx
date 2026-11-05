import GlassCard from '../common/GlassCard';
import { TriangleAlert, ShieldCheck, Info } from 'lucide-react';

const FLAGS = [
  { icon: TriangleAlert, tone: 'text-rose', title: 'Overlapping patent filed 2023', body: 'A similar claim structure was filed by a competitor two years ago.' },
  { icon: Info, tone: 'text-amber', title: 'Approach abandoned in 3 repos', body: 'Three public repositories using this architecture were archived without release.' },
  { icon: ShieldCheck, tone: 'text-cyan', title: 'Dataset license is compatible', body: 'The primary training dataset carries a permissive research-use license.' },
];

export default function RiskIntelligence() {
  return (
    <section className="px-4 py-20 sm:px-6 lg:py-28">
      <div className="mx-auto max-w-6xl">
        <div className="max-w-xl">
          <h2 className="font-display text-3xl text-text sm:text-4xl">
            Risk intelligence, not just a research summary.
          </h2>
          <p className="mt-4 text-text-dim">
            Revianta flags the things that quietly sink projects — before they've cost you
            a sprint, a hire, or a legal review.
          </p>
        </div>

        <div className="mt-12 grid gap-4 lg:grid-cols-3">
          {FLAGS.map(({ icon: Icon, tone, title, body }) => (
            <GlassCard key={title} className="p-6">
              <Icon size={20} className={tone} />
              <h3 className="mt-4 font-display text-[15px] text-text">{title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-text-dim">{body}</p>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>
  );
}
