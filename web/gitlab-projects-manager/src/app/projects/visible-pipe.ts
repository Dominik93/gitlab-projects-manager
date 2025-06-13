import { Pipe, PipeTransform } from '@angular/core';
import { Project } from './projects-component';

@Pipe({
  name: 'visible',
  pure: false
})
export class VisiblePipe implements PipeTransform {

  transform(value: Project[]): Project[] {
    if (!value) {
      return value;
    }

    return value.filter(p => p.visible);
  }

}
