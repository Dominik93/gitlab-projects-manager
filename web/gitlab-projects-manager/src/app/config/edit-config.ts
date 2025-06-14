import { Component, inject, Input } from '@angular/core';
import { ConfigService } from './config-service';
import { ErrorStatusService } from '../error-status/error-status-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-edit-config',
  imports: [FormsModule],
  templateUrl: './edit-config.html',
  styleUrl: './edit-config.css'
})
export class EditConfig {

  configService: ConfigService = inject(ConfigService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  @Input()
  name: string = "";

  content: string = "";

  ngOnInit() {
    this.configService.getConfig().subscribe(content => this.content = content)
  }

  onSave() {
    this.progressBarService.start();
    this.configService.saveConfig(this.content).subscribe({
      next: () => {
        this.progressBarService.stop()
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }

}
