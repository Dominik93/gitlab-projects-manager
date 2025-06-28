import { Component, inject } from '@angular/core';
import { EditConfig } from "./edit-config";
import { ProgressBarService } from '../progress-bar/progress-bar-service';

@Component({
  selector: 'app-config',
  imports: [EditConfig],
  templateUrl: './config.html',
  styleUrl: './config.css'
})
export class Config {

  loading = false;

  progressBarService: ProgressBarService = inject(ProgressBarService);

  ngOnInit(): void {
    this.progressBarService.loading().subscribe(isLoading => this.loading = isLoading);
  }
}
