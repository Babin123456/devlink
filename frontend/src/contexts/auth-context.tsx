import { useCallback, useEffect, useState } from "react";
import { api } from "@/api/client";
import { tokenStore } from "@/api/tokens";

export interface AuthUser {
  id: string;
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  [key: string]: unknown;
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);

  useEffect(() => {
    if (!tokenStore.getAccess()) {
      setUser(null);
      return;
    }
    let cancelled = false;
    api
      .get<AuthUser>("/api/users/me")
      .then((me) => {
        if (!cancelled) setUser(me);
      })
      .catch(() => {
        if (!cancelled) setUser(null);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    setUser(null);
  }, []);

  return { user, setUser, logout };
}
