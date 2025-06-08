import { Component, inject } from '@angular/core';
import { ProgressBarService } from './progress-bar-service';

@Component({
  selector: 'app-progress-bar',
  imports: [],
  templateUrl: './progress-bar.html',
  styleUrl: './progress-bar.css'
})
export class ProgressBar {

  progressBarService: ProgressBarService = inject(ProgressBarService)

  progress: number = 0;

  interval: any;

  loading = false;

  ngOnInit(): void {
    this.progressBarService.loading().subscribe(val => {
      if (val) {
        this.startLoading();
      } else {
        this.stopLoading();
      }
    })
  }

  startLoading() {
    this.loading = true;
    this.interval = setInterval(() => {
      if (this.progress > 100) {
        this.progress = 0;
      } else {
        this.progress += 5;
      }
    }, 500)
  }

  stopLoading() {
    this.progress = 0;
    this.loading = false;
    clearInterval(this.interval);
  }
}
