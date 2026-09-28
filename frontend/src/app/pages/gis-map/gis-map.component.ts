import { Component, OnInit, OnDestroy, AfterViewInit, ElementRef, ViewChild, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';
import * as L from 'leaflet';

import { ApiService } from '../../core/services/api.service';
import { ProjectGISMarker, GISFilterOptions } from '../../core/models/gis.model';

@Component({
  selector: 'app-gis-map',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './gis-map.component.html',
  styleUrl: './gis-map.component.scss'
})
export class GisMapComponent implements OnInit, AfterViewInit, OnDestroy {
  @ViewChild('mapContainer', { static: false }) mapContainer!: ElementRef<HTMLDivElement>;

  public markers = signal<ProjectGISMarker[]>([]);
  public filterOptions = signal<GISFilterOptions>({ states: [], districts: [], project_types: [], risk_levels: [] });
  public selectedMarker = signal<ProjectGISMarker | null>(null);
  public isLoading = signal<boolean>(true);

  // Filters
  public selectedState = signal<string>('');
  public selectedDistrict = signal<string>('');
  public selectedType = signal<string>('');
  public selectedRisk = signal<string>('');

  private map: L.Map | null = null;
  private markersLayer: L.LayerGroup | null = null;

  constructor(
    private apiService: ApiService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.loadFilterOptions();

    this.route.queryParamMap.subscribe(params => {
      const risk = params.get('risk');
      if (risk) {
        this.selectedRisk.set(risk.toUpperCase());
      }
      const state = params.get('state');
      if (state) {
        this.selectedState.set(state);
      }
      const pIdStr = params.get('projectId');
      const targetPId = pIdStr ? parseInt(pIdStr, 10) : undefined;
      this.fetchMarkers(targetPId);
    });
  }

  ngAfterViewInit(): void {
    this.initMap();
  }

  private initMap(): void {
    if (!this.mapContainer || this.map) return;

    // Centered on India (approx Lat 21.5, Lng 78.9) with zoom level 5
    this.map = L.map(this.mapContainer.nativeElement, {
      center: [21.5, 78.9],
      zoom: 5,
      zoomControl: true
    });

    // Standard OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(this.map);

    this.markersLayer = L.layerGroup().addTo(this.map);

    // If markers already loaded, render them
    if (this.markers().length > 0) {
      this.renderMarkersOnMap();
    }
  }

  public loadFilterOptions(): void {
    this.apiService.getGisFilters().subscribe({
      next: (opts) => this.filterOptions.set(opts),
      error: () => {}
    });
  }

  public fetchMarkers(targetProjectId?: number): void {
    this.isLoading.set(true);
    const filter = {
      state: this.selectedState() || undefined,
      district: this.selectedDistrict() || undefined,
      project_type: this.selectedType() || undefined,
      risk_level: this.selectedRisk() || undefined
    };

    this.apiService.getGisMarkers(filter).subscribe({
      next: (data) => {
        this.markers.set(data);
        this.isLoading.set(false);
        if (targetProjectId) {
          const match = data.find(m => m.id === targetProjectId);
          if (match) {
            this.selectedMarker.set(match);
          } else if (data.length > 0 && !this.selectedMarker()) {
            this.selectedMarker.set(data[0]);
          }
        } else if (data.length > 0 && !this.selectedMarker()) {
          this.selectedMarker.set(data[0]); // Select first marker for side panel
        }
        if (this.map) {
          this.renderMarkersOnMap(targetProjectId);
        }
      },
      error: (err) => {
        this.isLoading.set(false);
        console.error('Failed to load GIS markers:', err);
      }
    });
  }

  public onFilterChange(): void {
    this.fetchMarkers();
  }

  public resetFilters(): void {
    this.selectedState.set('');
    this.selectedDistrict.set('');
    this.selectedType.set('');
    this.selectedRisk.set('');
    this.fetchMarkers();
  }

  private renderMarkersOnMap(targetProjectId?: number): void {
    if (!this.map || !this.markersLayer) return;

    this.markersLayer.clearLayers();
    const bounds = L.latLngBounds([]);

    this.markers().forEach((m) => {
      const color = this.getMarkerColor(m.risk_level);
      const iconHtml = `
        <div style="
          background-color: ${color};
          width: 28px;
          height: 28px;
          border-radius: 50%;
          border: 3px solid #ffffff;
          box-shadow: 0 3px 8px rgba(0,0,0,0.35);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #ffffff;
          font-weight: 800;
          font-size: 11px;
        ">
          !
        </div>
      `;

      const customIcon = L.divIcon({
        className: 'custom-gis-pin',
        html: iconHtml,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const leafletMarker = L.marker([m.latitude, m.longitude], { icon: customIcon });

      // Tooltip on marker hover
      leafletMarker.bindTooltip(`
        <div style="font-family: system-ui, sans-serif; font-size: 11px;">
          <b>${m.project_code}</b>: ${m.name}<br/>
          <span style="color: ${color}; font-weight: 700;">${m.risk_level} RISK (+${m.predicted_delay_days}d delay)</span><br/>
          <small style="color: #4f46e5; font-weight: 600;">Click to open Project Details &rarr;</small>
        </div>
      `, { direction: 'top', offset: [0, -14] });

      // Popup Content on map pin
      const popupHtml = `
        <div style="min-width: 210px; font-family: system-ui, sans-serif; padding: 4px;">
          <div style="font-size: 11px; font-weight: 700; color: #4f46e5; margin-bottom: 2px;">${m.project_code}</div>
          <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">${m.name}</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 4px;"><b>District:</b> ${m.district}, ${m.state}</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 4px;"><b>Risk Score:</b> ${m.risk_score} / 100 (${m.risk_level})</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 8px;"><b>Predicted Delay:</b> +${m.predicted_delay_days} Days</div>
          <button id="popup-nav-${m.id}" style="
            display: inline-block;
            background: #4f46e5;
            color: #ffffff;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
          ">View Full Project Details &rarr;</button>
        </div>
      `;

      leafletMarker.bindPopup(popupHtml);

      leafletMarker.on('popupopen', () => {
        const btn = document.getElementById(`popup-nav-${m.id}`);
        if (btn) {
          btn.onclick = (e) => {
            e.preventDefault();
            this.navigateToProject(m.id);
          };
        }
      });

      // Direct navigation on clicking the risk project map marker (Requirement #3)
      leafletMarker.on('click', () => {
        this.selectedMarker.set(m);
        this.navigateToProject(m.id);
      });

      this.markersLayer!.addLayer(leafletMarker);
      bounds.extend([m.latitude, m.longitude]);
    });

    if (targetProjectId) {
      const target = this.markers().find(m => m.id === targetProjectId);
      if (target && this.map) {
        this.map.setView([target.latitude, target.longitude], 9, { animate: true });
        return;
      }
    }

    if (this.markers().length > 0 && bounds.isValid()) {
      this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 8 });
    }
  }

  public navigateToProject(id: number): void {
    this.router.navigate(['/projects', id]);
  }

  public selectMarkerFromList(m: ProjectGISMarker): void {
    this.selectedMarker.set(m);
    if (this.map) {
      this.map.setView([m.latitude, m.longitude], 8, { animate: true });
    }
  }

  private getMarkerColor(level: string): string {
    switch (level?.toUpperCase()) {
      case 'HIGH': return '#dc2626'; // Red
      case 'MEDIUM': return '#f59e0b'; // Amber
      case 'LOW': return '#10b981'; // Green
      default: return '#10b981';
    }
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
      this.map = null;
    }
  }
}
