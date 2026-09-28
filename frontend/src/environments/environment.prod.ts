export const environment = {
  production: true,
  apiUrl: (typeof window !== 'undefined' && (window as any).__env?.apiUrl)
    ? (window as any).__env.apiUrl
    : (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1')
      ? (window.location.port === '' || window.location.port === '80' || window.location.port === '443')
        ? `${window.location.origin}/api`
        : `${window.location.protocol}//${window.location.hostname}:8000/api`
      : 'http://localhost:8000/api'
};
