export const environment = {
  production: true,
  apiUrl: (typeof window !== 'undefined' && (window as any).__env?.apiUrl)
    ? (window as any).__env.apiUrl
    : 'https://sih-prototype-397y.onrender.com/api'
};
