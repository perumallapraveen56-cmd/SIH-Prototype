import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { ProjectsListComponent } from './pages/projects-list/projects-list.component';
import { ProjectDetailsComponent } from './pages/project-details/project-details.component';
import { GisMapComponent } from './pages/gis-map/gis-map.component';
import { AnalyticsComponent } from './pages/analytics/analytics.component';
import { ShapExplainabilityComponent } from './pages/shap-explainability/shap-explainability.component';
import { WhatIfAnalysisComponent } from './pages/what-if-analysis/what-if-analysis.component';
import { AlertsComponent } from './pages/alerts/alerts.component';
import { ReportsComponent } from './pages/reports/reports.component';
import { LandRecordsComponent } from './pages/land-records/land-records.component';
import { SettingsComponent } from './pages/settings/settings.component';

export const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full'
      },
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'projects',
        component: ProjectsListComponent,
        data: { criticalOnly: false }
      },
      {
        path: 'critical-projects',
        component: ProjectsListComponent,
        data: { criticalOnly: true }
      },
      {
        path: 'projects/:id',
        component: ProjectDetailsComponent
      },
      {
        path: 'gis-map',
        component: GisMapComponent
      },
      {
        path: 'risk-analysis',
        component: AnalyticsComponent
      },
      {
        path: 'analytics',
        component: AnalyticsComponent
      },
      {
        path: 'shap',
        component: ShapExplainabilityComponent
      },
      {
        path: 'what-if',
        component: WhatIfAnalysisComponent
      },
      {
        path: 'explainable-ai',
        component: WhatIfAnalysisComponent
      },
      {
        path: 'alerts',
        component: AlertsComponent
      },
      {
        path: 'reports',
        component: ReportsComponent
      },
      {
        path: 'land-records',
        component: LandRecordsComponent
      },
      {
        path: 'settings',
        component: SettingsComponent
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'dashboard'
  }
];
