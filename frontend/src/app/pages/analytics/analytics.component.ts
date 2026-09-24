import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { DashboardKPISummary, ProjectRiskOverviewChart } from '../../core/models/risk.model';
import { ProjectSummary } from '../../core/models/project.model';

interface StateAnalytics {
  state: string;
  total_projects: number;
  high_risk_count: number;
  avg_delay_days: number;
  total_cost_cr: number;
}

interface FactorPrevalence {
  factor: string;
  category: string;
  affected_projects: number;
  avg_delay_impact: number;
  severity: string;
}

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './analytics.component.html',
  styleUrl: './analytics.component.scss'
})
export class AnalyticsComponent implements OnInit {
  kpis = signal<DashboardKPISummary | null>(null);
  chartData = signal<ProjectRiskOverviewChart | null>(null);
  projects = signal<ProjectSummary[]>([]);
  isLoading = signal<boolean>(true);
  errorMessage = signal<string>('');

  stateBreakdown = computed<StateAnalytics[]>(() => {
    const list = this.projects();
    const map = new Map<string, { total: number; high: number; delaySum: number; costSum: number }>();

    for (const p of list) {
      const cur = map.get(p.state) || { total: 0, high: 0, delaySum: 0, costSum: 0 };
      cur.total += 1;
      if (p.risk_level === 'HIGH') cur.high += 1;
      cur.delaySum += p.predicted_delay_days;
      cur.costSum += (p.predicted_delay_days * p.daily_delay_cost_lakhs) / 100.0;
      map.set(p.state, cur);
    }

    return Array.from(map.entries()).map(([state, val]) => ({
      state,
      total_projects: val.total,
      high_risk_count: val.high,
      avg_delay_days: Math.round(val.delaySum / val.total),
      total_cost_cr: Math.round(val.costSum * 100) / 100
    })).sort((a, b) => b.total_cost_cr - a.total_cost_cr);
  });

  factorPrevalence = signal<FactorPrevalence[]>([
    { factor: 'Land Dispute Litigation Index', category: 'Judicial & Title', affected_projects: 9, avg_delay_impact: 42, severity: 'HIGH' },
    { factor: 'Section 19 Declaration Velocity', category: 'Statutory Gazetting', affected_projects: 8, avg_delay_impact: 38, severity: 'HIGH' },
    { factor: 'Compensation Rate Disparity Ratio', category: 'Financial & Awards', affected_projects: 7, avg_delay_impact: 31, severity: 'HIGH' },
    { factor: 'Cadastral Discrepancy & Mutation Lag', category: 'Revenue Records', affected_projects: 6, avg_delay_impact: 24, severity: 'MEDIUM' },
    { factor: 'Forest / Environmental Stage-II Clearances', category: 'Regulatory Environment', affected_projects: 5, avg_delay_impact: 29, severity: 'MEDIUM' },
    { factor: 'R&R Entitlement Package Acceptance', category: 'Social Rehabilitation', affected_projects: 4, avg_delay_impact: 18, severity: 'MEDIUM' },
    { factor: 'Gram Sabha / Tribal Consent Resolution', category: 'Public Consultation', affected_projects: 3, avg_delay_impact: 16, severity: 'LOW' },
    { factor: 'Utility Shifting & Right-of-Way Obstruction', category: 'Engineering Clearance', affected_projects: 3, avg_delay_impact: 12, severity: 'LOW' }
  ]);

  totalPortfolioExposureCr = computed(() => {
    const list = this.projects();
    const sum = list.reduce((acc, p) => acc + (p.predicted_delay_days * p.daily_delay_cost_lakhs) / 100.0, 0);
    return sum.toFixed(2);
  });

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadAnalytics();
  }

  loadAnalytics(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.apiService.getDashboardKPIs().subscribe({
      next: (k) => this.kpis.set(k),
      error: () => {}
    });

    this.apiService.getRiskOverviewChart().subscribe({
      next: (c) => this.chartData.set(c),
      error: () => {}
    });

    this.apiService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set('Could not fetch analytics data from backend.');
      }
    });
  }
}
