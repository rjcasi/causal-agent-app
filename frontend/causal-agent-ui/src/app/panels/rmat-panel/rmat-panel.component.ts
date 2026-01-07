import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgentService } from '../../services/agent.service';

@Component({
  selector: 'rmat-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rmat-panel.component.html',
  styleUrls: ['./rmat-panel.component.scss']
})
export class RmatPanelComponent {
  private agent = inject(AgentService);

  causalData: any = null;
  loading = false;
  error: string | null = null;

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
}