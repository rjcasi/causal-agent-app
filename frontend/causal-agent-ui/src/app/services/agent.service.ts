import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CausalResponse {
  chain: number[];
  antichain: number[];
}

@Injectable({ providedIn: 'root' })
export class AgentService {
  private http = inject(HttpClient);

  getRMATCausal(): Observable<CausalResponse> {
    return this.http.get<CausalResponse>('http://localhost:8000/rmat/causal');
  }
}