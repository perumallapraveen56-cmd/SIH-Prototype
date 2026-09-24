import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { ApiService } from '../../core/services/api.service';
import { SoundService } from '../../core/services/sound.service';
import { AuthService } from '../../core/services/auth.service';
import { AlertItem } from '../../core/models/alert.model';

@Component({
  selector: 'app-alerts',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './alerts.component.html',
  styleUrl: './alerts.component.scss'
})
export class AlertsComponent implements OnInit {
  public alerts = signal<AlertItem[]>([]);
  public filteredAlerts = signal<AlertItem[]>([]);
  public activeFilter = signal<string>('ALL');
  public isLoading = signal<boolean>(true);
  public isTriggeringLive = signal<boolean>(false);

  constructor(
    private apiService: ApiService,
    public soundService: SoundService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.loadAlerts();
  }

  loadAlerts(): void {
    this.isLoading.set(true);
    this.apiService.getAlerts().subscribe({
      next: (data) => {
        this.alerts.set(data);
        this.applyFilter(this.activeFilter());
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  applyFilter(filter: string): void {
    this.activeFilter.set(filter);
    if (filter === 'ALL') {
      this.filteredAlerts.set(this.alerts());
    } else if (filter === 'UNACKNOWLEDGED') {
      this.filteredAlerts.set(this.alerts().filter(a => !a.acknowledged));
    } else {
      this.filteredAlerts.set(this.alerts().filter(a => a.severity === filter));
    }
  }

  acknowledge(alert: AlertItem): void {
    const officerName = this.authService.currentUser()?.full_name || 'Revenue Officer';
    this.apiService.acknowledgeAlert(alert.alert_id, officerName).subscribe({
      next: (updated) => {
        this.alerts.update(list => list.map(a => a.alert_id === updated.alert_id ? updated : a));
        this.applyFilter(this.activeFilter());
      },
      error: (err) => console.error('Failed to acknowledge alert:', err)
    });
  }

  triggerDemoAlert(): void {
    this.isTriggeringLive.set(true);
    this.apiService.triggerLiveAlert().subscribe({
      next: (newAlert) => {
        this.soundService.playAlertSound();
        this.alerts.update(list => [newAlert, ...list]);
        this.applyFilter(this.activeFilter());
        this.isTriggeringLive.set(false);
      },
      error: () => this.isTriggeringLive.set(false)
    });
  }

  testAudio(): void {
    this.soundService.playAlertSound();
  }
}
