import { Component, EventEmitter, inject, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MavenService } from './maven-service';

export type BumpDependencyInput = {
  dependency?: string,
  version?: string,
  message?: string,
  branch?: string,
}

@Component({
  selector: 'app-maven',
  imports: [FormsModule],
  templateUrl: './maven.html',
  styleUrl: './maven.css'
})
export class Maven {

  mavenService: MavenService = inject(MavenService);

  @Input()
  name: string = ""

  @Input()
  namespace: string = ""

  @Output()
  bumpDependencyFired = new EventEmitter<BumpDependencyInput>();

  bumpDependencyInput: BumpDependencyInput = {};

  onVersionChanged($event: any) {
    this.bumpDependencyInput.branch = `feature/${this.bumpDependencyInput.dependency}_${$event}`;
    this.bumpDependencyInput.message = `bump ${this.bumpDependencyInput.dependency} ${$event}`;
  }

  onDependencyChanged($event: any) {
    this.bumpDependencyInput.branch = `feature/${$event}_${this.bumpDependencyInput.version}`;
    this.bumpDependencyInput.message = `bump ${$event} ${this.bumpDependencyInput.version}`;
  }

  bumpDependency() {
    this.bumpDependencyFired.emit(this.bumpDependencyInput);
  }

}
