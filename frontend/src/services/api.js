const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';

export class ApiError extends Error {
  constructor(message, { status, data } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.data = data;
  }
}

export async function request(path, { params, headers, body, ...options } = {}) {
  const url = new URL(BASE_URL.replace(/\/$/, '') + path, window.location.origin);

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, value);
      }
    });
  }

  const token =
    sessionStorage.getItem('revianta_access_token') ||
    localStorage.getItem('revianta_access_token');

  const requestHeaders = { Accept: 'application/json', ...headers };

  if (body !== undefined) requestHeaders['Content-Type'] = 'application/json';
  if (token) requestHeaders.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(url.toString(), {
      ...options,
      headers: requestHeaders,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch (error) {
    throw new ApiError(
      'Could not reach the Revianta AI backend. Check that the backend is running.',
      { status: 0, data: error }
    );
  }

  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json')
    ? await response.json().catch(() => null)
    : null;

  if (!response.ok) {
    throw new ApiError(
      payload?.detail || payload?.message || `Request failed (${response.status})`,
      { status: response.status, data: payload }
    );
  }

  return payload;
}

export const http = {
  get: (path, params) => request(path, { method: 'GET', params }),
  post: (path, body) => request(path, { method: 'POST', body }),
  put: (path, body) => request(path, { method: 'PUT', body }),
  patch: (path, body) => request(path, { method: 'PATCH', body }),
  delete: (path) => request(path, { method: 'DELETE' }),
};
