import { Component, OnInit, OnDestroy, AfterViewInit, ElementRef, ViewChild, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
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
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadFilterOptions();
    this.fetchMarkers();
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

  public fetchMarkers(): void {
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
        if (data.length > 0 && !this.selectedMarker()) {
          this.selectedMarker.set(data[0]); // Select first marker for side panel
        }
        if (this.map) {
          this.renderMarkersOnMap();
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

  private renderMarkersOnMap(): void {
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

      // Popup Content on map pin click
      const popupHtml = `
        <div style="min-width: 200px; font-family: system-ui, sans-serif; padding: 4px;">
          <div style="font-size: 11px; font-weight: 700; color: #4f46e5; margin-bottom: 2px;">${m.project_code}</div>
          <div style="font-size: 13px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">${m.name}</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 4px;"><b>District:</b> ${m.district}, ${m.state}</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 4px;"><b>Risk Score:</b> ${m.risk_score} / 100 (${m.risk_level})</div>
          <div style="font-size: 12px; color: #475569; margin-bottom: 8px;"><b>Predicted Delay:</b> +${m.predicted_delay_days} Days</div>
          <a href="/projects/${m.id}" style="
            display: inline-block;
            background: #4f46e5;
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-decoration: none;
          ">View Details &rarr;</a>
        </div>
      `;

      leafletMarker.bindPopup(popupHtml);

      leafletMarker.on('click', () => {
        this.selectedMarker.set(m);
      });

      this.markersLayer!.addLayer(leafletMarker);
      bounds.extend([m.latitude, m.longitude]);
    });

    if (this.markers().length > 0 && bounds.isValid()) {
      this.map.fitBounds(bounds, { padding: [50, 50], maxZoom: 8 });
    }
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
