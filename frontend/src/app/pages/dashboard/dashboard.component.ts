import { Component, OnInit, signal, computed, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { AuthService } from '../../core/services/auth.service';
import { DashboardKPISummary, ProjectRiskOverviewChart } from '../../core/models/risk.model';
import { ProjectSummary } from '../../core/models/project.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent implements OnInit {
  public kpis = signal<DashboardKPISummary | null>(null);
  public riskChartData = signal<ProjectRiskOverviewChart | null>(null);
  public recentProjects = signal<ProjectSummary[]>([]);
  public isLoading = signal<boolean>(true);
  public hasError = signal<boolean>(false);
  public errorMessage = signal<string>('');

  constructor(
    public authService: AuthService,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.isLoading.set(true);
    this.hasError.set(false);

    // Fetch all dashboard data from backend single source of truth
    this.apiService.getDashboardKPIs().subscribe({
      next: (kpiData) => {
        this.kpis.set(kpiData);
      },
      error: (err) => {
        this.hasError.set(true);
        this.errorMessage.set('Failed to connect to backend server. Please verify backend is running on port 8000.');
        this.isLoading.set(false);
      }
    });

    this.apiService.getRiskOverviewChart().subscribe({
      next: (chartData) => {
        this.riskChartData.set(chartData);
      },
      error: () => {}
    });

    this.apiService.getProjects().subscribe({
      next: (projects) => {
        this.recentProjects.set(projects);
        this.isLoading.set(false);
      },
      error: () => {
        this.isLoading.set(false);
      }
    });
  }

  getRiskBadgeClass(level: string): string {
    switch (level?.toUpperCase()) {
      case 'HIGH': return 'risk-high';
      case 'MEDIUM': return 'risk-medium';
      case 'LOW': return 'risk-low';
      default: return 'risk-low';
    }
  }
}
