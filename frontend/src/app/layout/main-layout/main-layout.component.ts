import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterModule } from '@angular/router';
import { Subscription, interval } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { SidebarComponent } from '../sidebar/sidebar.component';
import { HeaderComponent } from '../header/header.component';
import { ApiService } from '../../core/services/api.service';
import { SoundService } from '../../core/services/sound.service';
import { AlertItem } from '../../core/models/alert.model';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterModule, SidebarComponent, HeaderComponent],
  templateUrl: './main-layout.component.html',
  styleUrl: './main-layout.component.scss'
})
export class MainLayoutComponent implements OnInit, OnDestroy {
  public unreadAlertCount = signal<number>(0);
  public activeToastAlert = signal<AlertItem | null>(null);

  private pollSub: Subscription | null = null;

  constructor(
    private apiService: ApiService,
    private soundService: SoundService
  ) {}

  ngOnInit(): void {
    // Initial fetch
    this.pollAlerts();

    // Setup periodic polling every 15 seconds (Requirement #16 & #17)
    this.pollSub = interval(15000).pipe(
      switchMap(() => this.apiService.pollAlerts())
    ).subscribe({
      next: (res) => {
        this.unreadAlertCount.set(res.unacknowledged_high_count);

        // Sound Notification Safety Trigger (Requirement #17 & #18)
        if (res.should_play_sound) {
          this.soundService.playAlertSound();

          // Find the newest high alert to display in toast
          const newest = res.alerts.find(a => res.new_alert_ids.includes(a.alert_id));
          if (newest) {
            this.activeToastAlert.set(newest);
            setTimeout(() => this.activeToastAlert.set(null), 8000);
          }
        }
      },
      error: (err) => {
        console.warn('Alerts poll error:', err);
      }
    });
  }

  private pollAlerts(): void {
    this.apiService.pollAlerts().subscribe({
      next: (res) => {
        this.unreadAlertCount.set(res.unacknowledged_high_count);
        if (res.should_play_sound) {
          this.soundService.playAlertSound();
          const newest = res.alerts.find(a => res.new_alert_ids.includes(a.alert_id));
          if (newest) {
            this.activeToastAlert.set(newest);
            setTimeout(() => this.activeToastAlert.set(null), 8000);
          }
        }
      },
      error: () => {}
    });
  }

  dismissToast(): void {
    this.activeToastAlert.set(null);
  }

  ngOnDestroy(): void {
    if (this.pollSub) {
      this.pollSub.unsubscribe();
    }
  }
}
