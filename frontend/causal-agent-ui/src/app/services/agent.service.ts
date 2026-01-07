import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CausalResponse {
  events: number[];
  relations: Record<string, number[]>;
  chains: number[][];
  antichains: number[][];
}

@Injectable({ providedIn: 'root' })
export class AgentService {
  private http = inject(HttpClient);

  // -----------------------------------------------------
  // RMAT: GET CAUSAL SET
  // -----------------------------------------------------
  getRMATCausal(): Observable<CausalResponse> {
    return this.http.get<CausalResponse>(
      'http://localhost:8000/agent/rmat/causal'
    );
  }

  // -----------------------------------------------------
  // RMAT: STEP ENGINE
  // -----------------------------------------------------
  stepRMAT(input?: number[]) {
    return this.http.post(
      'http://localhost:8000/agent/rmat/step',
      input ? { input } : {}
    );
  }

  // -----------------------------------------------------
  // HEARTBEAT
  // -----------------------------------------------------
  getHeartbeat() {
    return this.http.get(
      'http://localhost:8000/agent/heartbeat'
    );
  }

  // -----------------------------------------------------
  // LOGS
  // -----------------------------------------------------
  getLogs() {
    return this.http.get(
      'http://localhost:8000/agent/logs'
    );
  }
}