import { Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SoundService {
  private audioCtx: AudioContext | null = null;
  public soundEnabled = signal<boolean>(true);

  constructor() {
    const saved = localStorage.getItem('sih26017_sound_enabled');
    if (saved !== null) {
      this.soundEnabled.set(saved === 'true');
    }
  }

  public toggleSound(): boolean {
    const next = !this.soundEnabled();
    this.setSoundEnabled(next);
    return next;
  }

  public setSoundEnabled(enabled: boolean): void {
    this.soundEnabled.set(enabled);
    localStorage.setItem('sih26017_sound_enabled', String(enabled));
    if (enabled && !this.audioCtx) {
      this.initAudioContext();
    }
  }

  private initAudioContext(): void {
    try {
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      if (AudioContextClass) {
        this.audioCtx = new AudioContextClass();
      }
    } catch (e) {
      console.warn('AudioContext could not be initialized:', e);
    }
  }

  public playAlertSound(): void {
    if (!this.soundEnabled()) {
      return;
    }

    try {
      if (!this.audioCtx) {
        this.initAudioContext();
      }

      if (this.audioCtx && this.audioCtx.state === 'suspended') {
        this.audioCtx.resume();
      }

      if (!this.audioCtx) return;

      const now = this.audioCtx.currentTime;

      // Two-tone warning alert chime (880Hz -> 659.25Hz harmonic decay)
      const osc1 = this.audioCtx.createOscillator();
      const osc2 = this.audioCtx.createOscillator();
      const gainNode = this.audioCtx.createGain();

      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(880, now); // A5 note
      osc1.frequency.exponentialRampToValueAtTime(440, now + 0.35);

      osc2.type = 'triangle';
      osc2.frequency.setValueAtTime(659.25, now + 0.1); // E5 note
      osc2.frequency.exponentialRampToValueAtTime(330, now + 0.45);

      gainNode.gain.setValueAtTime(0.35, now);
      gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.5);

      osc1.connect(gainNode);
      osc2.connect(gainNode);
      gainNode.connect(this.audioCtx.destination);

      osc1.start(now);
      osc2.start(now + 0.1);
      osc1.stop(now + 0.4);
      osc2.stop(now + 0.55);

    } catch (err) {
      console.warn('Audio notification could not play due to browser policy or context:', err);
    }
  }
}
