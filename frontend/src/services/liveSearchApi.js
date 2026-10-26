
/**
 * Revianta AI — live research search client.
 *
 * All external provider requests go through FastAPI.
 * Provider credentials remain on the backend.
 *
 * Expected endpoint:
 * GET /api/live-search?source=papers&q=...
 * GET /api/live-search?source=github&q=...
 * GET /api/live-search?source=datasets&q=...
 * GET /api/live-search?source=patents&q=...
 */

export class LiveSearchError extends Error {
  constructor(message, cause) {
    super(message);
    this.name = 'LiveSearchError';
    this.cause = cause;
  }
}

async function searchBackend(source, query, { limit = 10 } = {}) {
  const normalizedQuery = String(query ?? '').trim();

  if (!normalizedQuery) {
    throw new LiveSearchError('Enter a search query.');
  }

  const params = new URLSearchParams({
    source,
    q: normalizedQuery,
    limit: String(Math.max(1, Math.min(Number(limit) || 10, 25))),
  });

  let response;

  try {
    response = await fetch(`/api/live-search?${params.toString()}`);
  } catch (err) {
    throw new LiveSearchError(
      'Could not connect to the Revianta AI backend. Check that FastAPI is running.',
      err,
    );
  }

  let body;

  try {
    body = await response.json();
  } catch {
    body = {};
  }

  if (!response.ok) {
    throw new LiveSearchError(
      body.detail || `Live search failed (${response.status}).`,
    );
  }

  if (!Array.isArray(body.results)) {
    throw new LiveSearchError('The backend returned an unexpected search response.');
  }

  return body.results;
}

export function searchPapersLive(query, options = {}) {
  return searchBackend('papers', query, options);
}

export function searchGithubLive(query, options = {}) {
  return searchBackend('github', query, options);
}

export function searchDatasetsLive(query, options = {}) {
  return searchBackend('datasets', query, options);
}

export function searchPatentsLive(query, options = {}) {
  return searchBackend('patents', query, options);
}
