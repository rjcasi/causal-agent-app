import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgentService } from '../../services/agent.service';

@Component({
  selector: 'logs-panel',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './logs-panel.component.html',
  styleUrls: ['./logs-panel.component.scss']
})
export class LogsPanelComponent {
  private agent = inject(AgentService);

  logs: any = null;
  loading = false;
  error: string | null = null;

  loadLogs() {
    this.loading = true;
    this.error = null;

    this.agent.getLogs().subscribe({
      next: (data) => {
        this.logs = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load logs';
        this.loading = false;
      }
    });
  }
}
