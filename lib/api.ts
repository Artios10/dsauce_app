import { CreateUserParams, SignInParams, User } from "@/type";
import * as SecureStore from "expo-secure-store";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const AUTH_TOKENS_KEY = "dsauce_auth_tokens";

type AuthTokens = {
  access: string;
  refresh: string;
};

let authTokens: AuthTokens | null = null;
let tokensHydrated = false;

const persistTokens = async (tokens: AuthTokens | null) => {
  if (tokens) {
    await SecureStore.setItemAsync(AUTH_TOKENS_KEY, JSON.stringify(tokens));
    return;
  }

  await SecureStore.deleteItemAsync(AUTH_TOKENS_KEY);
};

const ensureTokensLoaded = async () => {
  if (tokensHydrated) return;

  const storedValue = await SecureStore.getItemAsync(AUTH_TOKENS_KEY);
  if (storedValue) {
    try {
      authTokens = JSON.parse(storedValue) as AuthTokens;
    } catch {
      authTokens = null;
    }
  }

  tokensHydrated = true;
};

const getErrorMessage = async (response: Response) => {
  let payload: unknown;

  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (payload && typeof payload === "object") {
    if ("detail" in payload && typeof payload.detail === "string") return payload.detail;

    const firstValue = Object.values(payload)[0];
    if (Array.isArray(firstValue) && typeof firstValue[0] === "string") return firstValue[0];
    if (typeof firstValue === "string") return firstValue;
  }

  return `Request failed with status ${response.status}`;
};

const refreshAccessToken = async () => {
  await ensureTokensLoaded();
  if (!authTokens?.refresh) return null;

  const response = await fetch(`${API_BASE_URL}/api/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: authTokens.refresh }),
  });

  if (!response.ok) {
    authTokens = null;
    await persistTokens(null);
    return null;
  }

  const data = (await response.json()) as { access: string };
  authTokens = { ...authTokens, access: data.access };
  await persistTokens(authTokens);
  return data.access;
};

const authenticatedFetch = async (path: string, init?: RequestInit) => {
  await ensureTokensLoaded();
  if (!authTokens?.access) throw new Error("Authentication required.");

  const request = async (token: string) =>
    fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(init?.headers ?? {}),
        Authorization: `Bearer ${token}`,
      },
    });

  let response = await request(authTokens.access);

  if (response.status === 401) {
    const refreshedToken = await refreshAccessToken();
    if (!refreshedToken) throw new Error("Session expired. Please sign in again.");
    response = await request(refreshedToken);
  }

  if (!response.ok) throw new Error(await getErrorMessage(response));
  return response;
};

export const createUser = async ({ email, password, name, role }: CreateUserParams) => {
  const registerResponse = await fetch(`${API_BASE_URL}/api/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password,
      username: name,
      role,
    }),
  });

  if (!registerResponse.ok) throw new Error(await getErrorMessage(registerResponse));

  await signIn({ email, password });
};

export const signIn = async ({ email, password }: SignInParams) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) throw new Error(await getErrorMessage(response));

  authTokens = (await response.json()) as AuthTokens;
  await persistTokens(authTokens);
};

export const getCurrentUser = async () => {
  const response = await authenticatedFetch("/api/auth/me/");
  return (await response.json()) as User;
};

export const getUsers = async () => {
  const response = await authenticatedFetch("/api/users/");
  const payload = (await response.json()) as { results?: User[] } | User[];
  if (Array.isArray(payload)) return payload;
  return payload.results ?? [];
};

export const getUser = async (id: number) => {
  const response = await authenticatedFetch(`/api/users/${id}/`);
  return (await response.json()) as User;
};

export const createUserAdmin = async (payload: {
  username: string;
  email: string;
  password: string;
  role: string;
  is_verified?: boolean;
  is_active?: boolean;
  is_staff?: boolean;
}) => {
  const response = await authenticatedFetch("/api/users/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return (await response.json()) as User;
};

export const updateUser = async (id: number, payload: Partial<{
  username: string;
  email: string;
  password: string;
  role: string;
  is_verified: boolean;
  is_active: boolean;
  is_staff: boolean;
}>) => {
  const response = await authenticatedFetch(`/api/users/${id}/`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
  return (await response.json()) as User;
};

export const deleteUser = async (id: number) => {
  await authenticatedFetch(`/api/users/${id}/`, {
    method: "DELETE",
  });
};

export const logout = async () => {
  await ensureTokensLoaded();

  if (!authTokens?.refresh) {
    authTokens = null;
    await persistTokens(null);
    return;
  }

  try {
    await fetch(`${API_BASE_URL}/api/auth/logout/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: authTokens.refresh }),
    });
  } finally {
    authTokens = null;
    await persistTokens(null);
  }
};
