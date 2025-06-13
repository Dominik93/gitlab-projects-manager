import { Component, inject, OnDestroy, OnInit } from '@angular/core';
import { ProgressBarService } from './progress-bar-service';

@Component({
  selector: 'app-progress-bar',
  imports: [],
  templateUrl: './progress-bar.html',
  styleUrl: './progress-bar.css'
})
export class ProgressBar implements OnInit, OnDestroy {

  progressBarService: ProgressBarService = inject(ProgressBarService);

  progress: number = 0;

  interval: any;

  loading = false;

  period = 500

  step = 5

  ngOnInit(): void {
    this.progressBarService.loading().subscribe(isLoading => {
      if (isLoading) {
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
        this.progress += this.step;
      }
    }, this.period)
  }

  stopLoading() {
    this.progress = 0;
    this.loading = false;
    clearInterval(this.interval);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }
  
}
