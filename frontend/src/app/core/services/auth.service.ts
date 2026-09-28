import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { User, AuthResponse } from '../models/user.model';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly apiUrl = environment.apiUrl;
  private readonly TOKEN_KEY = 'sih26017_token';
  private readonly USER_KEY = 'sih26017_user';

  public currentUser = signal<User | null>(this.getStoredUser());
  public isAuthenticated = computed(() => !!this.currentUser());
  public userRole = computed(() => this.currentUser()?.role || null);

  constructor(private http: HttpClient, private router: Router) {}

  private getStoredUser(): User | null {
    try {
      const stored = localStorage.getItem(this.USER_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  }

  public getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  public login(email: string, password: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/auth/login`, { email, password }).pipe(
      tap((res) => {
        localStorage.setItem(this.TOKEN_KEY, res.access_token);
        localStorage.setItem(this.USER_KEY, JSON.stringify(res.user));
        this.currentUser.set(res.user);
      })
    );
  }

  public loginDemo(role: 'Officer' | 'Analyst' | 'Admin'): Observable<AuthResponse> {
    const creds = {
      Officer: { email: 'officer@nexora.gov.in', password: 'Officer@123' },
      Analyst: { email: 'analyst@nexora.gov.in', password: 'Analyst@123' },
      Admin: { email: 'admin@nexora.gov.in', password: 'Admin@123' }
    }[role];

    return this.login(creds.email, creds.password);
  }

  public logout(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);
    this.currentUser.set(null);
    this.router.navigate(['/login']);
  }

  public hasRole(roles: string[]): boolean {
    const role = this.userRole();
    if (!role) return false;
    if (role === 'Admin') return true; // Admin has full access
    return roles.includes(role);
  }
}
