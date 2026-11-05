import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';
import AuthLayout from './AuthLayout';
import FormField from '../../components/common/FormField';
import GlowButton from '../../components/common/GlowButton';
import { useAuth } from '../../context/AuthContext';

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    const form = new FormData(event.currentTarget);
    const email = form.get('email')?.toString().trim();
    const password = form.get('password')?.toString();

    try {
      await login(email, password, remember);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    }
  }

  return (
    <AuthLayout eyebrow="Sign in" title="Welcome back" subtitle="Pick up where your research left off.">
      <form className="space-y-5" onSubmit={handleSubmit}>
        <FormField id="email" name="email" label="Email" type="email" placeholder="you@company.com" required />
        <FormField
          id="password"
          name="password"
          label="Password"
          type={showPassword ? 'text' : 'password'}
          placeholder="Enter your password"
          required
          trailing={
            <button type="button" onClick={() => setShowPassword((v) => !v)}
              className="text-text-faint hover:text-text-dim"
              aria-label={showPassword ? 'Hide password' : 'Show password'}>
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          }
        />
        <div className="flex items-center justify-between text-sm">
          <label className="flex items-center gap-2 text-text-dim">
            <input type="checkbox" checked={remember} onChange={(e) => setRemember(e.target.checked)}
              className="h-4 w-4 rounded border-line bg-white/[0.03] accent-indigo" />
            Remember me
          </label>
          <Link to="/forgot-password" className="text-indigo-soft hover:text-cyan">Forgot password?</Link>
        </div>
        {error && <p role="alert" className="text-sm text-red-400">{error}</p>}
        <GlowButton type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Log in'}
        </GlowButton>
      </form>
      <p className="mt-7 text-center text-sm text-text-dim">
        Don't have an account?{' '}
        <Link to="/register" className="font-medium text-indigo-soft hover:text-cyan">Create account</Link>
      </p>
    </AuthLayout>
  );
}
