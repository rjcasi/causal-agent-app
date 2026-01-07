import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'cockpit-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="cockpit">
      <aside class="sidebar">
        <h2>Agent Cockpit</h2>

        <nav>
          <a routerLink="/rmat" routerLinkActive="active">RMAT</a>
          <a routerLink="/heartbeat" routerLinkActive="active">Heartbeat</a>
          <a routerLink="/logs" routerLinkActive="active">Logs</a>
        </nav>
      </aside>

      <main class="panel-area">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .cockpit {
      display: flex;
      height: 100vh;
      background: #0d0d0d;
      color: #eee;
      font-family: monospace;
    }

    .sidebar {
      width: 220px;
      background: #111;
      padding: 1rem;
      border-right: 1px solid #333;
    }

    nav a {
      display: block;
      padding: 0.5rem 0;
      color: #ccc;
      text-decoration: none;
    }

    nav a.active {
      color: #fff;
      font-weight: bold;
    }

    .panel-area {
      flex: 1;
      padding: 1rem;
      overflow-y: auto;
    }
  `]
})
export class CockpitComponent {}