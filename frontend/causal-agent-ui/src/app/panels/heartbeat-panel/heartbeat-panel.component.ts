import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgentService } from '../../services/agent.service';

@Component({
  selector: 'heartbeat-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './heartbeat-panel.component.html',
  styleUrls: ['./heartbeat-panel.component.scss']
})
export class HeartbeatPanelComponent {
  private agent = inject(AgentService);

  heartbeat: any = null;
  loading = false;
  error: string | null = null;

  loadHeartbeat() {
    this.loading = true;
    this.error = null;

    this.agent.getHeartbeat().subscribe({
      next: (data) => {
        this.heartbeat = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load heartbeat';
        this.loading = false;
      }
    });
  }
}