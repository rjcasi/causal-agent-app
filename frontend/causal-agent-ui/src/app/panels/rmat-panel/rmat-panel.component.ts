import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgentService, CausalResponse } from '../../services/agent.service';

@Component({
  selector: 'rmat-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rmat-panel.component.html',
  styleUrls: ['./rmat-panel.component.scss']
})
export class RmatPanelComponent {

  private agent = inject(AgentService);

  causalData: CausalResponse | null = null;

  loading = false;
  stepLoading = false;
  error: string | null = null;

  // -----------------------------------------------------
  // LOAD CAUSAL SET
  // -----------------------------------------------------
  loadCausal() {
    this.loading = true;
    this.error = null;

    this.agent.getRMATCausal().subscribe({
      next: (data) => {
        this.causalData = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load RMAT causal-set data';
        this.loading = false;
      }
    });
  }

  // -----------------------------------------------------
  // STEP RMAT ENGINE
  // -----------------------------------------------------
  stepOnce() {
    this.stepLoading = true;
    this.error = null;

    this.agent.stepRMAT().subscribe({
      next: () => {
        this.stepLoading = false;
        this.loadCausal(); // refresh after stepping
      },
      error: () => {
        this.stepLoading = false;
        this.error = 'Failed to step RMAT engine';
      }
    });
  }
}