import { createContext, useContext, useMemo, useState } from 'react';
import { http } from '../services/api';

const AuthContext = createContext(null);
const TOKEN_KEY = 'revianta_access_token';
const USER_KEY = 'revianta_user';

function getSavedSession() {
  try {
    const token =
      sessionStorage.getItem(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY);
    const savedUser =
      sessionStorage.getItem(USER_KEY) || localStorage.getItem(USER_KEY);
    return { user: token && savedUser ? JSON.parse(savedUser) : null };
  } catch {
    return { user: null };
  }
}

function saveSession(data, remember = true) {
  clearSession();
  const storage = remember ? localStorage : sessionStorage;
  storage.setItem(TOKEN_KEY, data.access_token);
  storage.setItem(USER_KEY, JSON.stringify(data.user));
}

function clearSession() {
  sessionStorage.removeItem(TOKEN_KEY);
  sessionStorage.removeItem(USER_KEY);
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

export function AuthProvider({ children }) {
  const initial = useMemo(() => getSavedSession(), []);
  const [user, setUser] = useState(initial.user);
  const [isLoading, setIsLoading] = useState(false);

  async function login(email, password, remember = true) {
    setIsLoading(true);
    try {
      const data = await http.post('/auth/login', { email, password });
      saveSession(data, remember);
      setUser(data.user);
      return data.user;
    } finally {
      setIsLoading(false);
    }
  }

  async function register(name, email, password) {
    setIsLoading(true);
    try {
      const data = await http.post('/auth/register', { name, email, password });
      saveSession(data, true);
      setUser(data.user);
      return data.user;
    } finally {
      setIsLoading(false);
    }
  }

  async function logout() {
    try {
      await http.post('/auth/logout', {});
    } catch {
      // Always clear the local session, even if the API call fails.
    } finally {
      clearSession();
      setUser(null);
    }
  }

  const value = {
    user,
    isAuthenticated: Boolean(user),
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
