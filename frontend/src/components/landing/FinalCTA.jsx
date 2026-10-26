import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import GlowButton from '../common/GlowButton';
import GlassCard from '../common/GlassCard';

export default function FinalCTA() {
  return (
    <section className="px-4 py-20 sm:px-6 lg:py-28">
      <GlassCard tone="strong" glow="indigo" className="mx-auto max-w-5xl overflow-hidden p-10 text-center sm:p-16">
        <h2 className="font-display text-3xl text-text sm:text-4xl">
          Start with intelligence, not a blank page.
        </h2>
        <p className="mx-auto mt-4 max-w-md text-text-dim">
          Describe the project you're considering. Revianta maps the research landscape
          around it before you commit a single hour of build time.
        </p>
        <div className="mt-9 flex flex-wrap items-center justify-center gap-3">
          <GlowButton as={Link} to="/register" size="lg">
            Start a project
            <ArrowRight size={17} />
          </GlowButton>
          <GlowButton as={Link} to="/login" variant="ghost" size="lg">
            Log in
          </GlowButton>
        </div>
      </GlassCard>
    </section>
  );
}
