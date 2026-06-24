import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';

export type Role = 'teacher' | 'admin';

interface User {
  name: string;
  role: Role;
}

interface AuthState {
  user: User | null;
  role: Role | null;
  login: (role: Role, name?: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthState>({
  user: null,
  role: null,
  login: () => {},
  logout: () => {},
  isAuthenticated: false,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const saved = sessionStorage.getItem('xczs_user');
    return saved ? JSON.parse(saved) : null;
  });

  const login = useCallback((role: Role, name?: string) => {
    const u: User = { name: name || (role === 'admin' ? '管理员' : '张教授'), role };
    sessionStorage.setItem('xczs_user', JSON.stringify(u));
    setUser(u);
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem('xczs_user');
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, role: user?.role || null, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
