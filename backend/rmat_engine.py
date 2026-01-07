# backend/rmat_engine.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import math
import random

from causal_set import CausalSet


@dataclass
class RMATState:
    timestep: int
    spikes: List[float]
    density: List[float]
    attention: List[float]
    phase_space: List[float]  # concatenated [position..., momentum...]


class RecursiveMatrixAttentionTensor:
    """
    RMAT: a small, self-contained "organ" that:
    - evolves spikes, density, attention, and phase-space
    - grows a CausalSet one event per step
    - uses spike + attention to shape causal growth
    """

    def __init__(self, size: int = 4) -> None:
        self.size = size
        self.state = RMATState(
            timestep=0,
            spikes=[0.0] * size,
            density=[0.0] * size,
            attention=[0.0] * size,
            phase_space=[0.0] * (2 * size),
        )
        # Causal set organ
        self.causal = CausalSet()

        # initialize with one "genesis" event
        self.causal.add_event()

    # ------------------------------
    # PUBLIC API
    # ------------------------------

    def as_dict(self) -> dict:
        return {
            "timestep": self.state.timestep,
            "spikes": self.state.spikes,
            "density": self.state.density,
            "attention": self.state.attention,
            "phase_space": self.state.phase_space,
        }

    def step(self, external_input: Optional[List[float]] = None) -> RMATState:
        """
        Advance the RMAT by one timestep:
        - update spikes, density, attention, phase_space
        - grow the causal set (Smolin-style causal growth)
        """
        self.state.timestep += 1

        # 1. Update spikes (simple leaky integration + external input)
        new_spikes = []
        for i in range(self.size):
            base = self.state.spikes[i] * 0.7
            ext = 0.0
            if external_input and i < len(external_input):
                ext = external_input[i]
            val = base + 0.3 * ext
            # simple nonlinearity
            val = max(0.0, min(1.0, val))
            new_spikes.append(val)

        # 2. Update density (slow averaging of spikes)
        new_density = []
        for i in range(self.size):
            d = 0.9 * self.state.density[i] + 0.1 * new_spikes[i]
            new_density.append(d)

        # 3. Update attention (recursive function of spikes + density)
        new_attention = []
        for i in range(self.size):
            a_prev = self.state.attention[i]
            s = new_spikes[i]
            d = new_density[i]
            a = 0.8 * a_prev + 0.1 * s + 0.1 * (d - 0.5)
            new_attention.append(max(-1.0, min(1.0, a)))

        # 4. Update phase-space (toy Hamiltonian-like evolution)
        new_phase = self._update_phase_space(new_spikes, new_attention)

        self.state.spikes = new_spikes
        self.state.density = new_density
        self.state.attention = new_attention
        self.state.phase_space = new_phase

        # 5. Grow the causal set according to spike + attention
        self._grow_causal_set()

        return self.state

    # ------------------------------
    # INTERNAL DYNAMICS
    # ------------------------------

    def _update_phase_space(self, spikes: List[float], attention: List[float]) -> List[float]:
        """
        Very simple phase-space evolution:
        - positions x_i, momenta p_i
        - x' = x + p
        - p' = p + force(spikes, attention)
        """
        half = self.size
        x = self.state.phase_space[:half]
        p = self.state.phase_space[half:]

        new_x = []
        new_p = []

        for i in range(self.size):
            xi = x[i]
            pi = p[i]

            # force as function of spike/attention
            force = 0.2 * spikes[i] + 0.1 * attention[i]

            xi_new = xi + pi
            pi_new = 0.9 * pi + force

            new_x.append(xi_new)
            new_p.append(pi_new)

        return new_x + new_p

    def _grow_causal_set(self) -> None:
        """
        Smolin-inspired causal growth:
        - each step adds a new event
        - parents chosen probabilistically based on spikes + attention
        """

        # Create a new event for this timestep
        eid = self.causal.add_event()

        # If this is the first event, nothing to connect
        if eid == 0:
            return

        # Build weights from all previous events
        weights = []
        prev_events = list(range(eid))
        for ev in prev_events:
            idx = ev % self.size
            s = self.state.spikes[idx]
            a = self.state.attention[idx]
            w = max(0.0, 0.7 * s + 0.3 * (a + 1.0) / 2.0)  # a in [-1,1] -> [0,1]
            weights.append(w)

        total = sum(weights)

        if total <= 0:
            # no strong parents -> leave event almost isolated
            # optionally connect to immediate predecessor
            self.causal.add_relation(eid - 1, eid)
            return

        # normalize to probabilities
        probs = [w / total for w in weights]

        # sample between 1 and 3 parents
        num_parents = random.randint(1, min(3, len(prev_events)))

        parents = self._sample_parents(prev_events, probs, num_parents)

        for p in parents:
            self.causal.add_relation(p, eid)

    def _sample_parents(
        self,
        events: List[int],
        probs: List[float],
        k: int,
    ) -> List[int]:
        """
        Weighted sampling without replacement.
        """
        chosen = []
        available = events[:]
        p = probs[:]

        for _ in range(k):
            if not available:
                break
            r = random.random()
            cumulative = 0.0
            idx = 0
            for i, prob in enumerate(p):
                cumulative += prob
                if r <= cumulative:
                    idx = i
                    break
            chosen_event = available[idx]
            chosen.append(chosen_event)

            # remove chosen
            del available[idx]
            del p[idx]

            # renormalize remaining
            s = sum(p)
            if s > 0:
                p = [x / s for x in p]

        return chosen