import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { SoundService } from '../../core/services/sound.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
  @Input() unreadAlertsCount: number = 0;
  @Output() toggleSidebar = new EventEmitter<void>();

  constructor(
    public authService: AuthService,
    public soundService: SoundService
  ) {}

  onToggleSound(): void {
    const isNowOn = this.soundService.toggleSound();
    if (isNowOn) {
      this.soundService.playAlertSound(); // brief test chirp
    }
  }

  logout(): void {
    this.authService.logout();
  }
}
