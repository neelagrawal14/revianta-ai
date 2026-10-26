import { useState } from 'react';
import { User, Palette, Bell, FlaskConical, Database, ShieldCheck } from 'lucide-react';
import PageContainer from '../components/layout/PageContainer';
import GlassCard from '../components/common/GlassCard';
import GlowButton from '../components/common/GlowButton';
import { useAuth } from '../context/AuthContext';

const SECTIONS = [
  { id: 'profile', label: 'Profile', icon: User },
  { id: 'appearance', label: 'Appearance', icon: Palette },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'research', label: 'Research Preferences', icon: FlaskConical },
  { id: 'data', label: 'Data', icon: Database },
  { id: 'account', label: 'Account', icon: ShieldCheck },
];

function Toggle({ label, description, defaultOn = false }) {
  const [on, setOn] = useState(defaultOn);
  return (
    <div className="flex items-center justify-between gap-4 py-3">
      <div>
        <p className="text-sm text-text">{label}</p>
        {description && <p className="mt-0.5 text-xs text-text-faint">{description}</p>}
      </div>
      <button
        onClick={() => setOn((v) => !v)}
        aria-pressed={on}
        aria-label={label}
        className={`relative h-6 w-11 shrink-0 rounded-full transition-colors ${on ? 'bg-indigo' : 'bg-white/10'}`}
      >
        <span className={`absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform ${on ? 'translate-x-5' : 'translate-x-0.5'}`} />
      </button>
    </div>
  );
}

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <PageContainer>
      <p className="mono-tag text-indigo-soft">Workspace settings</p>
      <h1 className="mt-2 font-display text-3xl text-text sm:text-4xl">Settings</h1>

      <div className="mt-8 grid gap-6 lg:grid-cols-[220px_1fr]">
        <nav className="flex gap-2 overflow-x-auto lg:flex-col lg:overflow-visible">
          {SECTIONS.map((s) => (
            <a
              key={s.id}
              href={`#${s.id}`}
              className="flex shrink-0 items-center gap-2.5 rounded-xl px-3 py-2.5 text-sm text-text-dim hover:bg-white/[0.04] hover:text-text"
            >
              <s.icon size={15} /> {s.label}
            </a>
          ))}
        </nav>

        <div className="space-y-8">
          <GlassCard id="profile" className="p-6">
            <h2 className="font-display text-base text-text">Profile</h2>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              <div>
                <label className="mb-1.5 block text-sm text-text-dim">Name</label>
                <input
                  defaultValue={user?.name || 'Research Lead'}
                  className="h-11 w-full rounded-xl border border-line bg-white/[0.03] px-3.5 text-sm text-text focus:border-indigo/50 focus:outline-none"
                />
              </div>
              <div>
                <label className="mb-1.5 block text-sm text-text-dim">Email</label>
                <input
                  defaultValue={user?.email || 'you@company.com'}
                  className="h-11 w-full rounded-xl border border-line bg-white/[0.03] px-3.5 text-sm text-text focus:border-indigo/50 focus:outline-none"
                />
              </div>
            </div>
            <GlowButton size="sm" className="mt-5">Save changes</GlowButton>
          </GlassCard>

          <GlassCard id="appearance" className="p-6">
            <h2 className="font-display text-base text-text">Appearance</h2>
            <div className="mt-2 divide-y divide-line">
              <Toggle label="Reduce motion" description="Minimize animation across the interface" />
              <Toggle label="High-contrast mode" description="Increase contrast for readability" />
            </div>
          </GlassCard>

          <GlassCard id="notifications" className="p-6">
            <h2 className="font-display text-base text-text">Notifications</h2>
            <div className="mt-2 divide-y divide-line">
              <Toggle label="Analysis complete" description="Notify when a project's research intelligence finishes running" defaultOn />
              <Toggle label="New research gaps" description="Notify when Revianta flags a new gap in your domain" defaultOn />
              <Toggle label="Weekly digest" description="A weekly summary of workspace activity" />
            </div>
          </GlassCard>

          <GlassCard id="research" className="p-6">
            <h2 className="font-display text-base text-text">Research Preferences</h2>
            <div className="mt-2 divide-y divide-line">
              <Toggle label="Include preprints" description="Include arXiv and other preprint sources in search" defaultOn />
              <Toggle label="Prioritize open-access papers" description="Rank open-access sources higher in similarity search" />
            </div>
          </GlassCard>

          <GlassCard id="data" className="p-6">
            <h2 className="font-display text-base text-text">Data</h2>
            <p className="mt-1 text-sm text-text-dim">Export or remove your workspace data.</p>
            <div className="mt-4 flex flex-wrap gap-2">
              <GlowButton size="sm" variant="subtle">Export workspace data</GlowButton>
              <GlowButton size="sm" variant="subtle">Clear cached research</GlowButton>
            </div>
          </GlassCard>

          <GlassCard id="account" className="p-6">
            <h2 className="font-display text-base text-text">Account</h2>
            <p className="mt-1 text-sm text-text-dim">Manage your account and sign-in.</p>
            <GlowButton size="sm" variant="subtle" className="mt-4 text-rose">Delete account</GlowButton>
          </GlassCard>
        </div>
      </div>
    </PageContainer>
  );
}
