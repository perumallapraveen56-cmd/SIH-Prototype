import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';

import { ApiService } from '../../core/services/api.service';
import { RecommendationListResponse } from '../../core/models/recommendation.model';
import { WhatIfRequest, WhatIfResponse, FinancialImpactResponse } from '../../core/models/whatif.model';
import { ProjectSummary } from '../../core/models/project.model';

@Component({
  selector: 'app-what-if-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './what-if-analysis.component.html',
  styleUrl: './what-if-analysis.component.scss'
})
export class WhatIfAnalysisComponent implements OnInit {
  public recommendations = signal<RecommendationListResponse | null>(null);
  public simulationResult = signal<WhatIfResponse | null>(null);
  public financialImpact = signal<FinancialImpactResponse | null>(null);
  public allProjects = signal<ProjectSummary[]>([]);
  public selectedProjectId = signal<number>(1);

  // Intervention Sliders (0 - 100%)
  public compDelayPct = signal<number>(40);
  public legalDisputesPct = signal<number>(30);
  public approvalsExpeditedPct = signal<number>(35);
  public rrProgressPct = signal<number>(25);
  public docStreamlinePct = signal<number>(20);

  public isLoading = signal<boolean>(true);
  public isSimulating = signal<boolean>(false);
  public errorMessage = signal<string | null>(null);

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private apiService: ApiService
  ) {}

  ngOnInit(): void {
    // Load projects list for dropdown
    this.apiService.getProjects().subscribe({
      next: (projects) => this.allProjects.set(projects),
      error: () => {}
    });

    this.route.queryParams.subscribe((params) => {
      const pId = params['projectId'] ? parseInt(params['projectId'], 10) : 1;
      this.selectedProjectId.set(pId);
      this.loadAllData(pId);
    });
  }

  loadAllData(projectId: number): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    // 1. Load Recommendations
    this.apiService.getRecommendations(projectId).subscribe({
      next: (data) => this.recommendations.set(data),
      error: () => {}
    });

    // 2. Load Financial Impact Scenarios
    this.apiService.getFinancialImpact(projectId).subscribe({
      next: (data) => this.financialImpact.set(data),
      error: () => {}
    });

    // 3. Initial Baseline Simulation
    this.runSimulation();
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

  runSimulation(): void {
    this.isSimulating.set(true);
    const req: WhatIfRequest = {
      compensation_delay_reduction_pct: this.compDelayPct(),
      legal_disputes_resolution_pct: this.legalDisputesPct(),
      approvals_expedited_pct: this.approvalsExpeditedPct(),
      rr_progress_acceleration_pct: this.rrProgressPct(),
      documentation_streamlining_pct: this.docStreamlinePct()
    };

    this.apiService.runWhatIfSimulation(this.selectedProjectId(), req).subscribe({
      next: (res) => {
        this.simulationResult.set(res);
        this.isSimulating.set(false);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isSimulating.set(false);
        this.isLoading.set(false);
        this.errorMessage.set(err?.error?.detail || 'Simulation calculation failed on backend.');
      }
    });
  }

  resetSliders(): void {
    this.compDelayPct.set(0);
    this.legalDisputesPct.set(0);
    this.approvalsExpeditedPct.set(0);
    this.rrProgressPct.set(0);
    this.docStreamlinePct.set(0);
    this.runSimulation();
  }

  applyPreset(preset: 'aggressive' | 'moderate' | 'targeted'): void {
    if (preset === 'aggressive') {
      this.compDelayPct.set(70);
      this.legalDisputesPct.set(50);
      this.approvalsExpeditedPct.set(60);
      this.rrProgressPct.set(40);
      this.docStreamlinePct.set(50);
    } else if (preset === 'moderate') {
      this.compDelayPct.set(40);
      this.legalDisputesPct.set(30);
      this.approvalsExpeditedPct.set(35);
      this.rrProgressPct.set(25);
      this.docStreamlinePct.set(20);
    } else {
      this.compDelayPct.set(60);
      this.legalDisputesPct.set(0);
      this.approvalsExpeditedPct.set(45);
      this.rrProgressPct.set(10);
      this.docStreamlinePct.set(10);
    }
    this.runSimulation();
  }
}
