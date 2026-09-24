export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'Officer' | 'Analyst' | 'Admin';
  department?: string;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
