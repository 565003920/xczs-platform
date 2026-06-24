import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from 'react';

interface User {
  id: number;
  username: string;
  display_name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  role: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
  loading: boolean;
}

const AuthContext = createContext<AuthState>({
  user: null, token: null, role: null,
  login: async () => {}, logout: () => {},
  isAuthenticated: false, loading: true,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => sessionStorage.getItem('xczs_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { setLoading(false); return; }
    fetch('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } })
      .then(r => r.ok ? r.json() : Promise.reject())
      .then(u => { setUser(u); })
      .catch(() => { sessionStorage.removeItem('xczs_token'); setToken(null); })
      .finally(() => setLoading(false));
  }, []);

  const loginFn = useCallback(async (username: string, password: string) => {
    const r = await fetch('/api/auth/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!r.ok) { const err = await r.json(); throw new Error(err.detail || '登录失败'); }
    const data = await r.json();
    sessionStorage.setItem('xczs_token', data.token);
    setToken(data.token); setUser(data.user);
    // Set axios default header
    const m = await import('../api/client');
    m.default.defaults.headers.common['Authorization'] = `Bearer ${data.token}`;
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem('xczs_token'); setToken(null); setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{
      user, token, role: user?.role || null,
      login: loginFn, logout, isAuthenticated: !!user, loading,
    }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() { return useContext(AuthContext); }
