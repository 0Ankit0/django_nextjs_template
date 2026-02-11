export enum OAuthProvider {
  Google = 'google',
  Facebook = 'facebook',
}

export function startOAuthLogin(provider: OAuthProvider) {
  // Generate a random state for security
  const state = Math.random().toString(36).substring(7);
  sessionStorage.setItem('oauth_state', state);

  // Construct the backend OAuth URL
  // This matches the django-social-auth / python-social-auth endpoints
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

  // The actual endpoint usually involves directing to a backend view that redirects to the provider
  // Or verifying strictly on client side.
  // Assuming standard python-social-auth pattern: /login/<backend>/
  // But since we are using DRF and likely stateless JWT, the flow might be different.
  // For a standard Next.js + Django Social Auth setup:

  // We'll point to the Django backend's social login initiation endpoint
  // which will redirect the user to the provider.
  // Upon callback, the backend should handle the callback and redirect to frontend with tokens.

  const width = 500;
  const height = 600;
  const left = window.screen.width / 2 - width / 2;
  const top = window.screen.height / 2 - height / 2;

  // Assuming standard PSA URL pattern: /auth/login/<backend>/
  // Or custom endpoint. For now, let's use a generic structure that likely matches the backend.
  const authUrl = `${backendUrl}/auth/login/${provider}/?state=${state}`;

  window.open(
    authUrl,
    `Authenticate with ${provider}`,
    `width=${width},height=${height},left=${left},top=${top}`
  );
}
