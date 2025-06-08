import { Component, inject, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NamespaceService } from './namespace-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { ErrorStatusService } from '../error-status/error-status-service';

export type AddNamespaceInput = {
  name?: string,
  group?: string,
}
@Component({
  selector: 'app-add-namespace',
  imports: [FormsModule],
  templateUrl: './add-namespace.html',
  styleUrl: './add-namespace.css'
})
export class AddNamespace {

  namespaceService: NamespaceService = inject(NamespaceService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  @Input()
  name: string = ""

  addNamespaceInput: AddNamespaceInput = {};

  onAddNamespace() {
    this.progressBarService.startLoading()
    this.namespaceService.addNamespace(this.addNamespaceInput).subscribe({
      next: () => {
        this.progressBarService.stopLoading()
        this.errorStatusService.clear();
        this.namespaceService.added()
      },
      error: (res: any) => {
        this.progressBarService.stopLoading()
        this.errorStatusService.setError({ occured: true, httpMessage: res.message, message: res.error.message });
      }
    });
  }

}
