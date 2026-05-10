import { CreateUserParams, SignInParams, User } from "@/type";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type AuthTokens = {
  access: string;
  refresh: string;
};

let authTokens: AuthTokens | null = null;

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
  if (!authTokens?.refresh) return null;

  const response = await fetch(`${API_BASE_URL}/api/auth/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: authTokens.refresh }),
  });

  if (!response.ok) {
    authTokens = null;
    return null;
  }

  const data = (await response.json()) as { access: string };
  authTokens = { ...authTokens, access: data.access };
  return data.access;
};

const authenticatedFetch = async (path: string, init?: RequestInit) => {
  if (!authTokens?.access) throw new Error("Please sign in first.");

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

export const createUser = async ({ email, password, name }: CreateUserParams) => {
  const registerResponse = await fetch(`${API_BASE_URL}/api/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email,
      password,
      username: name,
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
};

export const getCurrentUser = async () => {
  const response = await authenticatedFetch("/api/auth/me/");
  return (await response.json()) as User;
};

export const logout = async () => {
  if (!authTokens?.refresh) {
    authTokens = null;
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
  }
};
