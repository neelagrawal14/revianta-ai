import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff } from 'lucide-react';
import AuthLayout from './AuthLayout';
import FormField from '../../components/common/FormField';
import GlowButton from '../../components/common/GlowButton';
import { useAuth } from '../../context/AuthContext';

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const { register, isLoading } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    const form = new FormData(event.currentTarget);
    const name = form.get('name')?.toString().trim();
    const email = form.get('email')?.toString().trim();
    const password = form.get('password')?.toString();
    const confirmPassword = form.get('confirmPassword')?.toString();

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      await register(name, email, password);
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
    }
  }

  return (
    <AuthLayout eyebrow="Create account" title="Start your research workspace"
      subtitle="A few details and you're mapping your first project.">
      <form className="space-y-5" onSubmit={handleSubmit}>
        <FormField id="name" name="name" label="Name" type="text" placeholder="Ada Researcher" required />
        <FormField id="email" name="email" label="Email" type="email" placeholder="you@company.com" required />
        <FormField id="password" name="password" label="Password"
          type={showPassword ? 'text' : 'password'} placeholder="Enter a password" required
          trailing={
            <button type="button" onClick={() => setShowPassword((v) => !v)}
              className="text-text-faint hover:text-text-dim"
              aria-label={showPassword ? 'Hide password' : 'Show password'}>
              {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
            </button>
          } />
        <FormField id="confirmPassword" name="confirmPassword" label="Confirm password"
          type={showPassword ? 'text' : 'password'} placeholder="Confirm your password" required />
        {error && <p role="alert" className="text-sm text-red-400">{error}</p>}
        <GlowButton type="submit" className="w-full" disabled={isLoading}>
          {isLoading ? 'Creating account...' : 'Create account'}
        </GlowButton>
      </form>
      <p className="mt-7 text-center text-sm text-text-dim">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-indigo-soft hover:text-cyan">Log in</Link>
      </p>
    </AuthLayout>
  );
}
