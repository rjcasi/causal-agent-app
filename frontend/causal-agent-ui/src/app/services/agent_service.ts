getRMATCausal() {
  return this.http.get(`${this.baseUrl}/agent/rmat/causal`);
}