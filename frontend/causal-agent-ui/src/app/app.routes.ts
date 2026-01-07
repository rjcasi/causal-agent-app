import { Routes } from '@angular/router';
import { RmatPanelComponent } from './panels/rmat-panel/rmat-panel.component';

export const routes: Routes = [
  { path: '', redirectTo: 'rmat', pathMatch: 'full' },
  { path: 'rmat', component: RmatPanelComponent }
];