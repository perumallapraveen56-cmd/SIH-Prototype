import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
import { AuthService } from '../../core/services/auth.service';
import { ProjectSummary } from '../../core/models/project.model';
import { LandParcel } from '../../core/models/parcel.model';

@Component({
  selector: 'app-land-records',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './land-records.component.html',
  styleUrl: './land-records.component.scss'
})
export class LandRecordsComponent implements OnInit {
  projects = signal<ProjectSummary[]>([]);
  allParcels = signal<LandParcel[]>([]);
  isLoading = signal<boolean>(true);
  errorMessage = signal<string>('');
  isMyParcelsOnly = signal<boolean>(false);

  // Search & Filters
  searchQuery = signal<string>('');
  selectedProjectId = signal<number | null>(null);
  selectedStage = signal<string>('ALL');
  selectedDispute = signal<string>('ALL');
  selectedParcel = signal<LandParcel | null>(null);

  stagesList = [
    'ALL',
    'Section 11 (Preliminary Notification)',
    'Section 19 (Declaration of Acquisition)',
    'Section 21 (Notice to Persons Interested)',
    'Section 23/30 (Enquiry & Award Declaration)',
    'Section 38 (Possession Taken)',
    'R&R Compensation Disbursed'
  ];

  baseParcels = computed(() => {
    const parcels = this.allParcels();
    if (!this.isMyParcelsOnly()) {
      return parcels;
    }
    // Filter to parcels in officer's jurisdiction (e.g. Uttar Pradesh, Gautam Buddha Nagar corridor)
    return parcels.filter(p =>
      p.state === 'Uttar Pradesh' ||
      p.district === 'Gautam Buddha Nagar' ||
      p.project_name.toLowerCase().includes('delhi-varanasi') ||
      p.project_name.toLowerCase().includes('jewar') ||
      p.project_code.includes('-UP-')
    );
  });

  filteredParcels = computed(() => {
    let parcels = this.baseParcels();
    const query = this.searchQuery().toLowerCase().trim();
    const projId = this.selectedProjectId();
    const stage = this.selectedStage();
    const dispute = this.selectedDispute();

    if (projId !== null) {
      parcels = parcels.filter(p => p.project_id === projId);
    }

    if (stage === 'IN_PROGRESS') {
      parcels = parcels.filter(p => !p.acquisition_stage.includes('Possession') && !p.acquisition_stage.includes('Disbursed'));
    } else if (stage !== 'ALL') {
      parcels = parcels.filter(p => p.acquisition_stage === stage);
    }

    if (dispute === 'DISPUTED') {
      parcels = parcels.filter(p => p.dispute_status.includes('Court') || p.dispute_status.includes('Writ') || p.dispute_status.includes('Dispute'));
    } else if (dispute === 'CLEAR') {
      parcels = parcels.filter(p => p.dispute_status.includes('Clear'));
    }

    if (query) {
      parcels = parcels.filter(p =>
        p.khasra_no.toLowerCase().includes(query) ||
        p.parcel_id.toLowerCase().includes(query) ||
        p.village.toLowerCase().includes(query) ||
        p.khatedar_owner.toLowerCase().includes(query) ||
        p.project_name.toLowerCase().includes(query)
      );
    }

    return parcels;
  });

  // KPI Computations based on current active scope
  totalParcelsCount = computed(() => this.baseParcels().length);
  disputedParcelsCount = computed(() =>
    this.baseParcels().filter(p => p.dispute_status.includes('Court') || p.dispute_status.includes('Writ') || p.dispute_status.includes('Dispute')).length
  );
  clearParcelsCount = computed(() =>
    this.baseParcels().filter(p => p.dispute_status.includes('Clear')).length
  );
  inProgressParcelsCount = computed(() =>
    this.baseParcels().filter(p => !p.acquisition_stage.includes('Possession') && !p.acquisition_stage.includes('Disbursed')).length
  );
  totalAreaHa = computed(() =>
    Math.round(this.baseParcels().reduce((acc, p) => acc + p.area_ha, 0) * 10) / 10
  );

  constructor(
    private apiService: ApiService,
    public authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParamMap.subscribe(params => {
      const myParcels = params.get('myParcels') || params.get('filter');
      if (myParcels === 'true' || myParcels === 'my-parcels') {
        this.isMyParcelsOnly.set(true);
      }
      const dispute = params.get('dispute');
      if (dispute) {
        this.selectedDispute.set(dispute.toUpperCase());
      }
      const stage = params.get('stage');
      if (stage) {
        this.selectedStage.set(stage);
      }
      const pId = params.get('projectId');
      if (pId) {
        this.selectedProjectId.set(parseInt(pId, 10));
      }
    });

    this.loadData();
  }

  setMyParcelsOnly(only: boolean): void {
    this.isMyParcelsOnly.set(only);
    this.resetFilters();
  }

  toggleMyParcels(): void {
    this.setMyParcelsOnly(!this.isMyParcelsOnly());
  }

  loadData(): void {
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.apiService.getProjects().subscribe({
      next: (projects) => this.projects.set(projects),
      error: () => {}
    });

    this.apiService.getLandParcels().subscribe({
      next: (parcels) => {
        this.allParcels.set(parcels);
        this.isLoading.set(false);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set('Could not fetch cadastral land records from the backend database.');
      }
    });
  }

  filterAll(): void {
    this.resetFilters();
  }

  filterDisputed(): void {
    this.selectedDispute.set('DISPUTED');
    this.selectedStage.set('ALL');
  }

  filterClear(): void {
    this.selectedDispute.set('CLEAR');
    this.selectedStage.set('ALL');
  }

  filterInProgress(): void {
    this.selectedDispute.set('ALL');
    this.selectedStage.set('IN_PROGRESS');
  }

  openParcelDetails(parcel: LandParcel): void {
    this.selectedParcel.set(parcel);
  }

  closeParcelDetails(): void {
    this.selectedParcel.set(null);
  }

  openParcelOnGis(parcel: LandParcel, event?: Event): void {
    if (event) event.stopPropagation();
    this.router.navigate(['/gis-map'], { queryParams: { projectId: parcel.project_id } });
  }

  resetFilters(): void {
    this.searchQuery.set('');
    this.selectedProjectId.set(null);
    this.selectedStage.set('ALL');
    this.selectedDispute.set('ALL');
  }
}
