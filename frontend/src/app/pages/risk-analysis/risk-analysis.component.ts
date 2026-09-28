import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { ProjectSummary, ProjectDetail } from '../../core/models/project.model';
import { ShapExplanationResponse } from '../../core/models/shap.model';

@Component({
  selector: 'app-risk-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './risk-analysis.component.html',
  styleUrl: './risk-analysis.component.scss'
})
export class RiskAnalysisComponent implements OnInit {
  projects = signal<ProjectSummary[]>([]);
  selectedProjectId = signal<number>(1);
  selectedProject = signal<ProjectDetail | null>(null);
  shapData = signal<ShapExplanationResponse | null>(null);
  isLoading = signal<boolean>(true);
  isLoadingDetail = signal<boolean>(false);
  errorMessage = signal<string>('');

  // Selected project diagnostics
  projectRiskScore = computed(() => this.selectedProject()?.risk_prediction?.risk_score || 0);
  projectDelayDays = computed(() => this.selectedProject()?.risk_prediction?.predicted_delay_days || 0);
  projectRiskLevel = computed(() => this.selectedProject()?.risk_prediction?.risk_level || 'HIGH');

  delayProbability = computed(() => {
    const score = this.projectRiskScore();
    return Math.min(99.4, Math.max(12.5, Math.round((score * 0.98 + 4.2) * 10) / 10));
  });

  dailyCostExposureLakhs = computed(() => this.selectedProject()?.daily_delay_cost_lakhs || 0);

  totalCostExposureCr = computed(() => {
    const p = this.selectedProject();
    if (!p) return 0;
    const delay = p.risk_prediction?.predicted_delay_days || 0;
    return Math.round(((delay * p.daily_delay_cost_lakhs) / 100.0) * 100) / 100;
  });

  highRiskPrioritizedProjects = computed(() => {
    return [...this.projects()].sort((a, b) => (b.risk_score || 0) - (a.risk_score || 0));
  });

  // RFCTLARR Stages progression checklist
  rfctlarrStages = [
    { name: 'Section 11 (Preliminary Notification)', code: 'SEC_11', standardDurationDays: 60 },
    { name: 'Section 19 (Declaration of Acquisition)', code: 'SEC_19', standardDurationDays: 90 },
    { name: 'Section 21 (Notice to Interested Persons)', code: 'SEC_21', standardDurationDays: 30 },
    { name: 'Section 23/30 (Enquiry & Award Declaration)', code: 'SEC_23', standardDurationDays: 120 },
    { name: 'Section 38 (Possession Handover)', code: 'SEC_38', standardDurationDays: 45 },
    { name: 'R&R Entitlement Disbursal', code: 'RR_DISBURSE', standardDurationDays: 60 }
  ];

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParamMap.subscribe(params => {
      const pId = params.get('projectId');
      const targetId = pId ? parseInt(pId, 10) : 1;
      this.selectedProjectId.set(targetId);
      this.loadProjects(targetId);
    });
  }

  loadProjects(targetProjectId: number): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.apiService.getProjects().subscribe({
      next: (projects) => {
        this.projects.set(projects);
        this.isLoading.set(false);

        const projectExists = projects.some(p => p.id === targetProjectId);
        const resolvedId = projectExists ? targetProjectId : (projects[0]?.id || 1);
        this.selectedProjectId.set(resolvedId);
        this.loadProjectDetails(resolvedId);
      },
      error: () => {
        this.isLoading.set(false);
        this.errorMessage.set('Could not fetch projects list from backend.');
      }
    });
  }

  selectProject(id: number): void {
    this.selectedProjectId.set(id);
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { projectId: id },
      queryParamsHandling: 'merge'
    });
    this.loadProjectDetails(id);
  }

  loadProjectDetails(id: number): void {
    this.isLoadingDetail.set(true);

    this.apiService.getProjectDetail(id).subscribe({
      next: (detail) => {
        this.selectedProject.set(detail);
        this.isLoadingDetail.set(false);
      },
      error: () => {
        this.isLoadingDetail.set(false);
        this.errorMessage.set(`Could not load details for project #${id}`);
      }
    });

    this.apiService.getShapAnalysis(id).subscribe({
      next: (shap) => {
        this.shapData.set(shap);
      },
      error: () => {
        // Fallback or non-fatal
      }
    });
  }

  isStageCompleted(stageName: string): boolean {
    const current = this.selectedProject()?.current_stage || '';
    const currentIndex = this.rfctlarrStages.findIndex(s => current.includes(s.code) || current.includes(s.name.substring(0, 10)));
    const targetIndex = this.rfctlarrStages.findIndex(s => s.name === stageName);
    return currentIndex > targetIndex;
  }

  isStageCurrent(stageName: string): boolean {
    const current = this.selectedProject()?.current_stage || '';
    return current.includes(stageName.substring(0, 10));
  }
}
