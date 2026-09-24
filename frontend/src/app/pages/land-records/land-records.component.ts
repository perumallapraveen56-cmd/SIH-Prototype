import { Component, OnInit, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ApiService } from '../../core/services/api.service';
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

  filteredParcels = computed(() => {
    let parcels = this.allParcels();
    const query = this.searchQuery().toLowerCase().trim();
    const projId = this.selectedProjectId();
    const stage = this.selectedStage();
    const dispute = this.selectedDispute();

    if (projId !== null) {
      parcels = parcels.filter(p => p.project_id === projId);
    }

    if (stage !== 'ALL') {
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

  // KPI Computations
  totalParcelsCount = computed(() => this.allParcels().length);
  disputedParcelsCount = computed(() =>
    this.allParcels().filter(p => p.dispute_status.includes('Court') || p.dispute_status.includes('Writ') || p.dispute_status.includes('Dispute')).length
  );
  clearParcelsCount = computed(() =>
    this.allParcels().filter(p => p.dispute_status.includes('Clear')).length
  );
  totalAreaHa = computed(() =>
    Math.round(this.allParcels().reduce((acc, p) => acc + p.area_ha, 0) * 10) / 10
  );

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadData();
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

  openParcelDetails(parcel: LandParcel): void {
    this.selectedParcel.set(parcel);
  }

  closeParcelDetails(): void {
    this.selectedParcel.set(null);
  }

  resetFilters(): void {
    this.searchQuery.set('');
    this.selectedProjectId.set(null);
    this.selectedStage.set('ALL');
    this.selectedDispute.set('ALL');
  }
}
