import { TestBed } from '@angular/core/testing';
import { App } from './app';

describe('App', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [App],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should have router-outlet element', () => {
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('router-outlet')).toBeTruthy();
  });
});

import { environment as prodEnv } from '../environments/environment.prod';

describe('Production Environment Configuration', () => {
  it('should be configured for production', () => {
    expect(prodEnv.production).toBe(true);
  });

  it('should use the production Render backend API URL and never localhost or port 8000', () => {
    expect(prodEnv.apiUrl).toBe('https://sih-prototype-397y.onrender.com/api');
    expect(prodEnv.apiUrl).not.toContain('localhost');
    expect(prodEnv.apiUrl).not.toContain('127.0.0.1');
    expect(prodEnv.apiUrl).not.toContain(':8000');
  });
});

