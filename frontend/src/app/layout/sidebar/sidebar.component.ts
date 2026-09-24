import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';

interface NavItem {
  label: string;
  route: string;
  icon: string;
  badge?: string;
  roles?: string[];
}

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  navItems: NavItem[] = [
    { label: 'Dashboard', route: '/dashboard', icon: 'ri-dashboard-line' },
    { label: 'Projects', route: '/projects', icon: 'ri-folder-shared-line' },
    { label: 'GIS Map', route: '/gis-map', icon: 'ri-map-pin-line' },
    { label: 'Risk Analysis', route: '/risk-analysis', icon: 'ri-shield-flash-line' },
    { label: 'Analytics', route: '/analytics', icon: 'ri-line-chart-line' },
    { label: 'AI Insights / SHAP', route: '/shap', icon: 'ri-brain-line' },
    { label: 'Critical Projects', route: '/critical-projects', icon: 'ri-alarm-warning-line' },
    { label: 'Alerts', route: '/alerts', icon: 'ri-notification-3-line' },
    { label: 'Reports', route: '/reports', icon: 'ri-file-chart-line' },
    { label: 'Land Records', route: '/land-records', icon: 'ri-survey-line' },
    { label: 'Settings', route: '/settings', icon: 'ri-settings-4-line' }
  ];

  constructor(public authService: AuthService) {}
}
