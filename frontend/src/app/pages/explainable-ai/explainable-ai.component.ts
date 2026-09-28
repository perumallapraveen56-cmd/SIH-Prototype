import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { ApiService } from '../../core/services/api.service';
import { ProjectDetail, ProjectSummary } from '../../core/models/project.model';
import { ShapExplanationResponse } from '../../core/models/shap.model';
import { RecommendationListResponse } from '../../core/models/recommendation.model';
import { FinancialImpactResponse } from '../../core/models/whatif.model';

export interface AdministrativeDelegation {
  level: string;
  designation: string;
  statutoryRef: string;
  slaWindow: string;
}

@Component({
  selector: 'app-explainable-ai',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './explainable-ai.component.html',
  styleUrl: './explainable-ai.component.scss'
})
export class ExplainableAiComponent implements OnInit {
  public project = signal<ProjectDetail | null>(null);
  public shapData = signal<ShapExplanationResponse | null>(null);
  public recommendations = signal<RecommendationListResponse | null>(null);
  public financialImpact = signal<FinancialImpactResponse | null>(null);
  public allProjects = signal<ProjectSummary[]>([]);
  public selectedProjectId = signal<number>(1);

  public isLoading = signal<boolean>(true);
  public errorMessage = signal<string | null>(null);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    // 1. Fetch projects list for corridor selector dropdown
    this.apiService.getProjects().subscribe({
      next: (projects) => this.allProjects.set(projects),
      error: () => {}
    });

    // 2. Read query params (preserve active project)
    this.route.queryParams.subscribe((params) => {
      const pId = params['projectId'] ? parseInt(params['projectId'], 10) : 1;
      this.selectedProjectId.set(pId);
      this.loadAllData(pId);
    });
  }

  loadAllData(projectId: number): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    let completedRequests = 0;
    const totalRequests = 4;
    const checkComplete = () => {
      completedRequests++;
      if (completedRequests >= totalRequests) {
        this.isLoading.set(false);
      }
    };

    // 1. Project Details
    this.apiService.getProjectDetail(projectId).subscribe({
      next: (data) => {
        this.project.set(data);
        checkComplete();
      },
      error: (err) => {
        this.errorMessage.set(err?.error?.detail || `Project #${projectId} details could not be loaded.`);
        checkComplete();
      }
    });

    // 2. SHAP Attribution
    this.apiService.getShapAnalysis(projectId).subscribe({
      next: (data) => {
        this.shapData.set(data);
        checkComplete();
      },
      error: () => checkComplete()
    });

    // 3. Actionable Recommendations
    this.apiService.getRecommendations(projectId).subscribe({
      next: (data) => {
        this.recommendations.set(data);
        checkComplete();
      },
      error: () => checkComplete()
    });

    // 4. Financial Impact Scenarios
    this.apiService.getFinancialImpact(projectId).subscribe({
      next: (data) => {
        this.financialImpact.set(data);
        checkComplete();
      },
      error: () => checkComplete()
    });
  }

  onProjectChange(newId: number): void {
    this.selectedProjectId.set(newId);
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { projectId: newId },
      queryParamsHandling: 'merge'
    });
    this.loadAllData(newId);
  }

  returnToShap(): void {
    this.router.navigate(['/shap'], { queryParams: { projectId: this.selectedProjectId() } });
  }

  navigateToProject(): void {
    this.router.navigate(['/projects', this.selectedProjectId()]);
  }

  navigateToWhatIf(): void {
    this.router.navigate(['/what-if'], { queryParams: { projectId: this.selectedProjectId() } });
  }

  simulateRecommendation(rec: any): void {
    this.router.navigate(['/what-if'], {
      queryParams: {
        projectId: this.selectedProjectId(),
        category: rec.category
      }
    });
  }

  getResponsibleAuthority(category: string): AdministrativeDelegation {
    const cat = category?.toLowerCase() || '';
    if (cat.includes('comp') || cat.includes('disburs') || cat.includes('award')) {
      return {
        level: 'District Level',
        designation: 'District Collector & Special Land Acquisition Officer (SLAO)',
        statutoryRef: 'RFCTLARR Act 2013 • Section 19/23 Award Notice',
        slaWindow: '14 Working Days'
      };
    } else if (cat.includes('legal') || cat.includes('dispute') || cat.includes('court')) {
      return {
        level: 'Judicial / State Level',
        designation: 'Lok Adalat Special Bench & State Legal Services Authority (SLSA)',
        statutoryRef: 'RFCTLARR Act 2013 • Section 64 Reference & ADR Mechanism',
        slaWindow: '21 Working Days'
      };
    } else if (cat.includes('approv') || cat.includes('forest') || cat.includes('statut') || cat.includes('clear')) {
      return {
        level: 'State / Central Level',
        designation: 'Principal Chief Conservator of Forests (PCCF) / MoEFCC Nodal Cell',
        statutoryRef: 'Forest (Conservation) Act Stage-II & PARIVESH Nodal Mandate',
        slaWindow: '30 Working Days'
      };
    } else if (cat.includes('r&r') || cat.includes('rehab') || cat.includes('resettl')) {
      return {
        level: 'Divisional Level',
        designation: 'Revenue Divisional Commissioner (RDC) & R&R Administrator',
        statutoryRef: 'RFCTLARR Act 2013 • Chapter V Rehabilitation Scheme',
        slaWindow: '28 Working Days'
      };
    } else if (cat.includes('doc') || cat.includes('record') || cat.includes('title')) {
      return {
        level: 'Tehsil / Sub-Divisional Level',
        designation: 'Tehsildar & District Land Sub-Registrar',
        statutoryRef: 'BhoomiRashi Digital Land Records Integration',
        slaWindow: '10 Working Days'
      };
    } else {
      return {
        level: 'Project Executing Level',
        designation: 'Project Director & Nodal Land Acquisition Cell',
        statutoryRef: 'Inter-Agency Fast-Track Coordination Committee',
        slaWindow: '15 Working Days'
      };
    }
  }

  getRiskSeverityClass(severity?: string): string {
    switch (severity?.toUpperCase()) {
      case 'HIGH': return 'risk-high';
      case 'MEDIUM': return 'risk-medium';
      case 'LOW': return 'risk-low';
      default: return 'risk-low';
    }
  }

  getPriorityBadgeClass(priority?: string): string {
    switch (priority?.toUpperCase()) {
      case 'CRITICAL': return 'priority-critical';
      case 'HIGH': return 'priority-high';
      case 'MEDIUM': return 'priority-medium';
      default: return 'priority-low';
    }
  }
}
