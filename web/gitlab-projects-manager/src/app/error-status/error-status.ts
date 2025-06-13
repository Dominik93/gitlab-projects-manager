import { Component, inject } from '@angular/core';
import { ErrorStatusService } from './error-status-service';

export type ErrorStatusData = {
  httpMessage: string,
  message: string
}

export function emptyError() { return { occured: false, httpMessage: "", message: "" } }

@Component({
  selector: 'app-error-status',
  imports: [],
  templateUrl: './error-status.html',
  styleUrl: './error-status.css'
})
export class ErrorStatus {

  errorStatusService: ErrorStatusService = inject(ErrorStatusService);

  error: ErrorStatusData = emptyError();

  ngOnInit(): void {
    this.errorStatusService.getError().subscribe(error => {
      this.error = error
    })
  }
}
