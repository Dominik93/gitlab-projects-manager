import { Component, inject } from '@angular/core';
import { ErrorStatusService } from '../error-status/error-status-service';
import { ProgressBarService } from '../progress-bar/progress-bar-service';
import { NamespaceService } from './namespace-service';
import { AddNamespace } from "./add-namespace";

@Component({
  selector: 'app-namespace',
  imports: [AddNamespace],
  templateUrl: './namespace.html',
  styleUrl: './namespace.css'
})
export class Namespace {

  namespaceService: NamespaceService = inject(NamespaceService);

  progressBarService: ProgressBarService = inject(ProgressBarService);

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  namespaces: string[] = [];

  selectedNamespace = "";

  loading = false;

  ngOnInit(): void {
    this.fetchNamespaces();
    this.progressBarService.loading().subscribe(isLoading => this.loading = isLoading);
    this.namespaceService.namespaceAdded().subscribe(() => this.fetchNamespaces());
  }

  onSelectNamespace(name: string) {
    this.selectedNamespace = name;
    this.namespaceService.select(this.selectedNamespace);
  }

  onDelete() {
    this.progressBarService.start();
    this.namespaceService.delete(this.selectedNamespace).subscribe(
      {
        next: () => {
          this.progressBarService.stop()
          this.errorStatusService.clear();
          this.selectedNamespace = "";
          this.fetchNamespaces();
        },
        error: (errorResponse: any) => {
          this.progressBarService.stop()
          this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
        }
      });
  }

  private fetchNamespaces() {
    this.progressBarService.start();
    this.namespaceService.getNamespaces().subscribe({
      next: (namespaces) => {
        this.progressBarService.stop()
        this.errorStatusService.clear();
        this.namespaces = namespaces
      },
      error: (errorResponse: any) => {
        this.progressBarService.stop()
        this.errorStatusService.set({ httpMessage: errorResponse.message, message: errorResponse.error.message });
      }
    });
  }
}
