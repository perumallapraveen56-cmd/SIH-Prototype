import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { ApiService } from '../../core/services/api.service';
import { ShapExplanationResponse } from '../../core/models/shap.model';
import { ProjectSummary } from '../../core/models/project.model';

@Component({
  selector: 'app-shap-explainability',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './shap-explainability.component.html',
  styleUrl: './shap-explainability.component.scss'
})
export class ShapExplainabilityComponent implements OnInit {
  public shapData = signal<ShapExplanationResponse | null>(null);
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
    // Load all projects for context switcher dropdown
    this.apiService.getProjects().subscribe({
      next: (projects) => {
        this.allProjects.set(projects);
      },
      error: () => {}
    });

    // Read query param if passed from Project Details (Requirement #11: "Do NOT lose selected project context")
    this.route.queryParams.subscribe((params) => {
      const pId = params['projectId'] ? parseInt(params['projectId'], 10) : 1;
      this.selectedProjectId.set(pId);
      this.loadShap(pId);
    });
  }

  loadShap(projectId: number): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.apiService.getShapAnalysis(projectId).subscribe({
      next: (data) => {
        this.shapData.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(err?.error?.detail || `SHAP explanation could not be retrieved for Project #${projectId}.`);
      }
    });
  }

  onProjectChange(newId: number): void {
    this.selectedProjectId.set(newId);
    this.router.navigate([], {
      relativeTo: this.route,
      queryParams: { projectId: newId },
      queryParamsHandling: 'merge'
    });
    this.loadShap(newId);
  }

  navigateToWhatIf(): void {
    const data = this.shapData();
    const pId = data ? data.project_id : this.selectedProjectId();
    this.router.navigate(['/what-if'], { queryParams: { projectId: pId } });
  }

  getRiskSeverityClass(level: string): string {
    switch (level?.toUpperCase()) {
      case 'HIGH': return 'risk-high';
      case 'MEDIUM': return 'risk-medium';
      case 'LOW': return 'risk-low';
      default: return 'risk-low';
    }
  }
}
