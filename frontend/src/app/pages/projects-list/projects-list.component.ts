import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
import { ProjectSummary } from '../../core/models/project.model';

@Component({
  selector: 'app-projects-list',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './projects-list.component.html',
  styleUrl: './projects-list.component.scss'
})
export class ProjectsListComponent implements OnInit {
  projects = signal<ProjectSummary[]>([]);
  isLoading = signal<boolean>(true);
  errorMessage = signal<string>('');
  isCriticalOnly = signal<boolean>(false);

  // Filters
  searchQuery = signal<string>('');
  selectedState = signal<string>('ALL');
  selectedType = signal<string>('ALL');
  selectedRisk = signal<string>('ALL');
  sortBy = signal<string>('risk_desc');

  availableStates = signal<string[]>([]);
  availableTypes = signal<string[]>([]);

  filteredProjects = computed(() => {
    let list = this.projects();
    const query = this.searchQuery().toLowerCase().trim();
    const state = this.selectedState();
    const type = this.selectedType();
    const risk = this.selectedRisk();

    if (this.isCriticalOnly()) {
      list = list.filter(p => p.risk_level === 'HIGH');
    } else if (risk !== 'ALL') {
      list = list.filter(p => p.risk_level === risk);
    }

    if (state !== 'ALL') {
      list = list.filter(p => p.state === state);
    }

    if (type !== 'ALL') {
      list = list.filter(p => p.project_type === type);
    }

    if (query) {
      // Support phonetic aliases (e.g. Kuthampur -> Udhampur)
      const alias = query.replace(/kuthampur/gi, 'udhampur');
      list = list.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.name.toLowerCase().includes(alias) ||
        p.project_code.toLowerCase().includes(query) ||
        p.district.toLowerCase().includes(query) ||
        p.state.toLowerCase().includes(query)
      );
    }

    // Sorting
    return [...list].sort((a, b) => {
      switch (this.sortBy()) {
        case 'risk_desc': return b.risk_score - a.risk_score;
        case 'delay_desc': return b.predicted_delay_days - a.predicted_delay_days;
        case 'cost_desc':
          return (b.predicted_delay_days * b.daily_delay_cost_lakhs) - (a.predicted_delay_days * a.daily_delay_cost_lakhs);
        case 'progress_asc': return a.acquisition_progress - b.acquisition_progress;
        default: return 0;
      }
    });
  });

  constructor(
    private apiService: ApiService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Check if this route is for critical projects
    this.route.data.subscribe(data => {
      this.isCriticalOnly.set(!!data['criticalOnly']);
    });

    // Support query parameters (e.g. /projects?risk=HIGH, /projects?sort=delay_desc, /projects?state=Maharashtra)
    this.route.queryParamMap.subscribe(params => {
      const risk = params.get('risk');
      if (risk) {
        this.selectedRisk.set(risk.toUpperCase());
      }
      const state = params.get('state');
      if (state) {
        this.selectedState.set(state);
      }
      const sort = params.get('sort');
      if (sort) {
        if (sort === 'cost') this.sortBy.set('cost_desc');
        else if (sort === 'delay') this.sortBy.set('delay_desc');
        else if (sort === 'risk') this.sortBy.set('risk_desc');
        else if (sort === 'progress') this.sortBy.set('progress_asc');
        else this.sortBy.set(sort);
      }
      const search = params.get('search');
      if (search) {
        this.searchQuery.set(search);
      }
    });

    this.loadProjects();
  }

  navigateToProject(id: number): void {
    this.router.navigate(['/projects', id]);
  }

  loadProjects(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.apiService.getProjects().subscribe({
      next: (data) => {
        this.projects.set(data);
        const states = Array.from(new Set(data.map(p => p.state))).sort();
        const types = Array.from(new Set(data.map(p => p.project_type))).sort();
        this.availableStates.set(states);
        this.availableTypes.set(types);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set('Failed to connect to backend server. Please verify backend is running.');
      }
    });
  }

  getCostImpactCr(project: ProjectSummary): string {
    const cost = (project.predicted_delay_days * project.daily_delay_cost_lakhs) / 100.0;
    return cost.toFixed(2);
  }

  resetFilters(): void {
    this.searchQuery.set('');
    this.selectedState.set('ALL');
    this.selectedType.set('ALL');
    this.selectedRisk.set('ALL');
    this.sortBy.set('risk_desc');
  }
}
