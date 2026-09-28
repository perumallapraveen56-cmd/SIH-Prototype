import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { ProjectSummary } from '../../core/models/project.model';
import { ReportGenerateRequest, ReportSummaryItem } from '../../core/models/report.model';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.scss'
})
export class ReportsComponent implements OnInit {
  projects = signal<ProjectSummary[]>([]);
  isLoading = signal<boolean>(false);
  isDownloading = signal<boolean>(false);
  isRefreshing = signal<boolean>(false);
  successMessage = signal<string>('');
  errorMessage = signal<string>('');
  activePreview = signal<any | null>(null);

  // Form Model
  selectedReportType: 'PROJECT_RISK' | 'DISTRICT_RISK' | 'STATE_RISK' | 'AI_EXPLAINABILITY' = 'PROJECT_RISK';
  selectedProjectId: number = 1;
  selectedState: string = 'Uttar Pradesh';
  selectedDistrict: string = 'Gautam Buddha Nagar';
  selectedFormat: 'pdf' | 'json' = 'pdf';

  // Available Filter Options
  availableStates: string[] = ['Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Gujarat', 'Haryana', 'Tamil Nadu', 'West Bengal', 'Telangana'];
  availableDistricts: string[] = ['Gautam Buddha Nagar', 'Pune', 'Bengaluru Urban', 'Ahmedabad', 'Gurugram', 'Kanchipuram', 'North 24 Parganas', 'Hyderabad'];

  // Pre-generated Audit Reports List for immediate demo and review
  archivedReports = signal<ReportSummaryItem[]>([
    {
      report_id: 'REP-2026-001',
      title: 'Delhi-Varanasi HSR Corridor (Package 2) - Detailed Risk Audit',
      report_type: 'PROJECT_RISK',
      generated_at: '2026-09-24 10:30 IST',
      summary: 'High risk detected due to Section 19 notification bottlenecks and 14 pending compensation writ petitions in Allahabad HC.',
      key_metrics: { 'Predicted Delay': '142 Days', 'Cost Impact': '₹6.39 Cr', 'Disputed Parcels': '28' },
      recommendations_count: 4,
      high_risk_flag: true
    },
    {
      report_id: 'REP-2026-002',
      title: 'Western Dedicated Freight Corridor (Dadri-JNPT) - AI Explainability Audit',
      report_type: 'AI_EXPLAINABILITY',
      generated_at: '2026-09-24 09:15 IST',
      summary: 'TreeSHAP attribution verified. Top contributing factor is Land Dispute Litigation Index (+0.38 contribution).',
      key_metrics: { 'Confidence Score': '94.2%', 'SHAP Factors': '8 Canonical', 'Model': 'CatBoost GBDT' },
      recommendations_count: 3,
      high_risk_flag: true
    },
    {
      report_id: 'REP-2026-003',
      title: 'Maharashtra State Expressway & Metro Land Acquisition Summary',
      report_type: 'STATE_RISK',
      generated_at: '2026-09-23 16:45 IST',
      summary: 'Statewide analysis of 4 active mega-projects covering 480 hectares across Pune, Raigad, and Thane districts.',
      key_metrics: { 'Total Projects': '4', 'Avg Delay': '88 Days', 'Total Exposure': '₹18.4 Cr' },
      recommendations_count: 5,
      high_risk_flag: false
    },
    {
      report_id: 'REP-2026-004',
      title: 'Bengaluru Urban District Cadastral Parcel Clearance Digest',
      report_type: 'DISTRICT_RISK',
      generated_at: '2026-09-22 14:20 IST',
      summary: 'Gram Sabha consent resolution pending for 18 parcels in Bengaluru Suburban Rail Project Corridor.',
      key_metrics: { 'Pending Parcels': '18', 'Avg Processing': '210 Days', 'Risk Level': 'MEDIUM' },
      recommendations_count: 2,
      high_risk_flag: false
    }
  ]);

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    const curId = this.selectedProjectId;
    this.apiService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data);
        if (data.some(p => p.id === curId)) {
          this.selectedProjectId = curId;
        } else if (data.length > 0) {
          this.selectedProjectId = data[0].id;
        }
      },
      error: (err) => console.warn('Could not load projects for reports:', err)
    });
  }

  refreshData(): void {
    if (this.isRefreshing()) return;
    this.isRefreshing.set(true);
    this.errorMessage.set('');

    const curId = this.selectedProjectId;
    this.apiService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data);
        if (data.some(p => p.id === curId)) {
          this.selectedProjectId = curId;
        } else if (data.length > 0) {
          this.selectedProjectId = data[0].id;
        }
        this.isRefreshing.set(false);
        this.successMessage.set('Report catalog and project data refreshed successfully from the backend database.');
        setTimeout(() => this.successMessage.set(''), 4000);
      },
      error: (err) => {
        this.isRefreshing.set(false);
        this.errorMessage.set('Failed to refresh report data from backend server.');
        setTimeout(() => this.errorMessage.set(''), 5000);
      }
    });
  }

  generateReport(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const req: ReportGenerateRequest = {
      report_type: this.selectedReportType,
      export_format: this.selectedFormat,
      project_id: this.selectedReportType === 'PROJECT_RISK' || this.selectedReportType === 'AI_EXPLAINABILITY' ? Number(this.selectedProjectId) : undefined,
      state: this.selectedReportType === 'STATE_RISK' ? this.selectedState : undefined,
      district: this.selectedReportType === 'DISTRICT_RISK' ? this.selectedDistrict : undefined
    };

    if (this.selectedFormat === 'pdf') {
      this.isDownloading.set(true);
      // Trigger PDF streaming download as Blob
      this.apiService.generateReport(req).subscribe({
        next: (blob: Blob) => {
          this.isLoading.set(false);
          this.isDownloading.set(false);
          const filename = `${this.selectedReportType.toLowerCase()}_report_${Date.now()}.pdf`;
          this.triggerBlobDownload(blob, filename);
          this.successMessage.set(`Official PDF report for ${this.selectedReportType} successfully generated and downloaded.`);
          setTimeout(() => this.successMessage.set(''), 6000);
        },
        error: (err) => {
          this.isLoading.set(false);
          this.isDownloading.set(false);
          this.errorMessage.set('Failed to generate report. Please ensure the backend server is active.');
        }
      });
    } else {
      // JSON data preview
      this.apiService.generateReport(req).subscribe({
        next: (data) => {
          this.isLoading.set(false);
          this.activePreview.set(data);
          this.successMessage.set('JSON Report Dossier generated successfully.');
          setTimeout(() => this.successMessage.set(''), 5000);
        },
        error: (err) => {
          this.isLoading.set(false);
          this.errorMessage.set('Failed to generate JSON report data.');
        }
      });
    }
  }

  downloadDirectProjectPdf(projectId: number): void {
    this.isDownloading.set(true);
    this.apiService.downloadProjectReportPdf(projectId).subscribe({
      next: (blob: Blob) => {
        this.isDownloading.set(false);
        const filename = `Project_Risk_Report_PRJ_${projectId}.pdf`;
        this.triggerBlobDownload(blob, filename);
        this.successMessage.set(`Project #${projectId} PDF report downloaded successfully.`);
        setTimeout(() => this.successMessage.set(''), 5000);
      },
      error: () => {
        this.isDownloading.set(false);
        this.errorMessage.set(`Could not generate PDF for Project #${projectId}.`);
      }
    });
  }

  private triggerBlobDownload(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  viewArchivedReport(report: ReportSummaryItem): void {
    this.activePreview.set(report);
  }

  closePreview(): void {
    this.activePreview.set(null);
  }
}
