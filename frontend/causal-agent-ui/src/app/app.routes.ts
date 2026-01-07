import { Routes } from '@angular/router';

import { CockpitComponent } from './cockpit/cockpit';
import { RmatPanelComponent } from './panels/rmat-panel/rmat-panel.component';
import { HeartbeatPanelComponent } from './panels/heartbeat-panel/heartbeat-panel.component';
import { LogsPanelComponent } from './panels/logs-panel/logs-panel.component';

export const routes: Routes = [
  {
    path: '',
    component: CockpitComponent,
    children: [
      { path: 'rmat', component: RmatPanelComponent },
      { path: 'heartbeat', component: HeartbeatPanelComponent },
      { path: 'logs', component: LogsPanelComponent },

      { path: '', redirectTo: 'rmat', pathMatch: 'full' }
    ]
  }
];