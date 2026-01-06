from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from datetime import datetime


@dataclass
class RMATState:
    timestep: int = 0

    # Causal set (very simple: adjacency counts)
    causal_matrix: List[List[float]] = field(default_factory=list)

    # Spike layer (simple list of activations)
    spikes: List[float] = field(default_factory=list)

    # Flow, density, phase-space projections (1D for now)
    flow: List[float] = field(default_factory=list)
    density: List[float] = field(default_factory=list)
    phase_space: List[float] = field(default_factory=list)

    # Recursive attention tensor (flattened view)
    attention: List[float] = field(default_factory=list)


class RecursiveMatrixAttentionTensor:
    """
    RMAT: a simplified, evolving core.
    This is the 'brainstem' we can deepen later with real math.
    """

    def __init__(self, size: int = 4):
        self.size = size
        self.state = self._init_state()

    def _init_state(self) -> RMATState:
        n = self.size
        return RMATState(
            timestep=0,
            causal_matrix=[[0.0 for _ in range(n)] for _ in range(n)],
            spikes=[0.0 for _ in range(n)],
            flow=[0.0 for _ in range(n)],
            density=[0.0 for _ in range(n)],
            phase_space=[0.0 for _ in range(2 * n)],
            attention=[0.0 for _ in range(n)],
        )

    def _stdp_update(self, spikes: List[float]) -> List[float]:
        # Simple STDP-like update: strengthen active spikes, decay others
        return [
            s * 0.95 + 0.1 if s > 0.2 else s * 0.9
            for s in spikes
        ]

    def _flow_update(self, flow: List[float]) -> List[float]:
        # Simple flow: shift and decay
        if not flow:
            return flow
        shifted = flow[1:] + [flow[0]]
        return [0.9 * x for x in shifted]

    def _density_update(self, density: List[float], spikes: List[float]) -> List[float]:
        # Density responds to spikes, then diffuses slightly
        return [
            0.8 * d + 0.3 * s
            for d, s in zip(density, spikes)
        ]

    def _phase_space_update(self, phase_space: List[float], attention: List[float]) -> List[float]:
        # Interpret phase_space as [position..., momentum...]
        n = len(phase_space) // 2
        pos = phase_space[:n]
        mom = phase_space[n:]

        pos = [p + 0.05 * a for p, a in zip(pos, attention)]
        mom = [m * 0.95 + 0.02 * a for m, a in zip(mom, attention)]

        return pos + mom

    def _recursive_attention(self, state: RMATState) -> List[float]:
        """
        Very simplified 'R(A) = A - mu(A) + zeta(A) - gamma(A)' idea,
        implemented as local/global mixing.
        """
        att = state.attention
        if not att:
            return att

        avg = sum(att) / len(att)
        # 'mu' inversion-ish: center around average
        centered = [a - avg for a in att]

        # 'zeta' accumulation-ish: running sum influence
        running = []
        total = 0.0
        for c in centered:
            total += c
            running.append(total)

        # 'gamma' normalization-ish: squash
        max_abs = max(abs(x) for x in running) or 1.0
        return [x / max_abs for x in running]

    def step(self, external_input: List[float] | None = None) -> RMATState:
        """
        Advance the RMAT one timestep.
        external_input can be interpreted as new spikes.
        """
        s = self.state
        n = self.size

        if external_input is None:
            external_input = [0.0 for _ in range(n)]
        else:
            external_input = list(external_input)[:n] + [0.0] * max(0, n - len(external_input))

        # Update spikes with external input + STDP-like rule
        new_spikes = [max(0.0, min(1.0, es + 0.5 * inp)) for es, inp in zip(s.spikes, external_input)]
        new_spikes = self._stdp_update(new_spikes)

        # Update flow and density based on spikes
        new_flow = self._flow_update(s.flow)
        new_density = self._density_update(s.density, new_spikes)

        # Update phase space based on attention
        new_attention = [0.6 * a + 0.4 * s for a, s in zip(s.attention, new_spikes)] if s.attention else new_spikes[:]
        new_phase_space = self._phase_space_update(s.phase_space, new_attention)

        # Recursive attention refinement
        tmp_state = RMATState(
            timestep=s.timestep + 1,
            causal_matrix=s.causal_matrix,  # we’ll evolve this later
            spikes=new_spikes,
            flow=new_flow,
            density=new_density,
            phase_space=new_phase_space,
            attention=new_attention,
        )
        refined_attention = self._recursive_attention(tmp_state)
        tmp_state.attention = refined_attention

        self.state = tmp_state
        return self.state

    def as_dict(self) -> Dict[str, Any]:
        s = self.state
        return {
            "timestep": s.timestep,
            "size": self.size,
            "spikes": s.spikes,
            "flow": s.flow,
            "density": s.density,
            "phase_space": s.phase_space,
            "attention": s.attention,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }