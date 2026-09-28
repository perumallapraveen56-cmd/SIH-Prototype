import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { ProjectDetail } from '../../core/models/project.model';

@Component({
  selector: 'app-project-details',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './project-details.component.html',
  styleUrl: './project-details.component.scss'
})
export class ProjectDetailsComponent implements OnInit {
  public project = signal<ProjectDetail | null>(null);
  public isLoading = signal<boolean>(true);
  public errorMessage = signal<string | null>(null);
  public isDownloadingPdf = signal<boolean>(false);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const idParam = params.get('id');
      const id = idParam ? parseInt(idParam, 10) : 1;
      this.loadProject(id);
    });
  }

  loadProject(id: number): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.apiService.getProjectDetail(id).subscribe({
      next: (data) => {
        this.project.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(err?.error?.detail || `Project #${id} could not be loaded.`);
      }
    });
  }

  navigateToShap(): void {
    const p = this.project();
    if (p) {
      this.router.navigate(['/shap'], { queryParams: { projectId: p.id } });
    }
  }

  navigateToWhatIf(): void {
    const p = this.project();
    if (p) {
      this.router.navigate(['/what-if'], { queryParams: { projectId: p.id } });
    }
  }

  navigateToSimulate(): void {
    this.navigateToWhatIf();
  }

  downloadPdfReport(): void {
    const p = this.project();
    if (!p) return;
    this.isDownloadingPdf.set(true);
    const url = this.apiService.downloadProjectReportPdfUrl(p.id);
    window.open(url, '_blank');
    setTimeout(() => this.isDownloadingPdf.set(false), 2000);
  }

  getRiskSeverityClass(severity: string): string {
    switch (severity?.toUpperCase()) {
      case 'HIGH': return 'risk-high';
      case 'MEDIUM': return 'risk-medium';
      case 'LOW': return 'risk-low';
      default: return 'risk-low';
    }
  }
}
