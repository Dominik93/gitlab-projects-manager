import { Injectable } from '@angular/core';
import { Project } from './projects-component';



@Injectable({
  providedIn: 'root'
})
export class VisibleFilterService {

  filter(value: Project[]): Project[] {
    if (!value) {
      return value;
    }

    return value.filter(p => p.visible);
  }

}
