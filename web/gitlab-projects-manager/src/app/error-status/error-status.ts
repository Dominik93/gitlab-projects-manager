import { Component, inject } from '@angular/core';
import { ErrorStatusService } from './error-status-service';

export type ErrorStatusData = {
  occured: boolean,
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

  error: ErrorStatusData = emptyError();

  errorStatusService: ErrorStatusService = inject(ErrorStatusService)


  ngOnInit(): void {
    this.errorStatusService.getError().subscribe(val => {
      this.error = val
    })
  }
}
