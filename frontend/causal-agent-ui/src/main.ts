import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { routes } from './app/app.routes';
import { CockpitComponent } from './app/cockpit/cockpit';

bootstrapApplication(CockpitComponent, {
  providers: [provideRouter(routes)]
}).catch(err => console.error(err));