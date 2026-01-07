# backend/main.py

from datetime import datetime
from typing import Optional, Dict, Any, List

from fastapi import FastAPI

from rmat_engine import RecursiveMatrixAttentionTensor

app = FastAPI()

# Single RMAT instance for the backend
rmat = RecursiveMatrixAttentionTensor(size=4)


# -----------------------------------
# BASIC HEALTH / HEARTBEAT
# -----------------------------------

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.get("/agent/heartbeat")
def agent_heartbeat() -> Dict[str, Any]:
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/agent/status")
def agent_status() -> Dict[str, Any]:
    return {
        "heartbeat": True,
        "logs": [
            "Agent initialized",
            "RMAT engine online",
            "Causal set organ active",
            "Awaiting tasks",
        ],
        "modules": {
            "fuzzer": "idle",
            "defense": "ready",
            "symbolic_core": "initializing",
            "rmat": "active",
            "causal_set": "growing",
        },
    }


# -----------------------------------
# RMAT ORGAN ENDPOINTS
# -----------------------------------

@app.get("/agent/rmat/state")
def rmat_state() -> Dict[str, Any]:
    """
    Return the current RMAT state without advancing time.
    """
    return {"state": rmat.as_dict()}


@app.post("/agent/rmat/step")
def rmat_step(payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Advance the RMAT engine one timestep.
    Optional: pass {"input": [...]} to drive spikes.
    """
    external_input: Optional[List[float]] = None
    if payload and "input" in payload:
        external_input = payload["input"]

    state = rmat.step(external_input=external_input)
    return {"state": rmat.as_dict()}


@app.get("/agent/rmat/view")
def rmat_view() -> Dict[str, Any]:
    """
    A simplified RMAT state for cockpit visualization.
    """
    s = rmat.state
    half = rmat.size
    return {
        "timestep": s.timestep,
        "spikes": s.spikes,
        "density": s.density,
        "attention": s.attention,
        "phase_space": {
            "position": s.phase_space[:half],
            "momentum": s.phase_space[half:],
        },
    }


@app.get("/agent/rmat/causal")
def rmat_causal() -> Dict[str, Any]:
    """
    Returns a cockpit-friendly view of the causal set:
    - events
    - relations (causal arrows)
    - chains (greedy)
    - antichains (simple level slicing)
    """

    cset = rmat.causal

    # JSON-safe relations (string keys)
    relations = {str(k): v for k, v in cset.relations.items()}

    # Build chains (greedy)
    chains: List[List[int]] = []
    visited = set()

    for e in cset.events:
        if e in visited:
            continue

        chain = [e]
        visited.add(e)

        current = e
        while True:
            fut = cset.future_of(current)
            if len(fut) == 1:
                nxt = fut[0]
                if nxt in visited:
                    break
                chain.append(nxt)
                visited.add(nxt)
                current = nxt
            else:
                break

        chains.append(chain)

    # Build antichains (simple slicing)
    antichains: List[List[int]] = []
    remaining = set(cset.events)

    while remaining:
        slice_set: List[int] = []
        for e in list(remaining):
            if all(
                not (
                    e in cset.future_of(x)
                    or x in cset.future_of(e)
                )
                for x in slice_set
            ):
                slice_set.append(e)
                remaining.remove(e)
        antichains.append(slice_set)

    return {
        "events": cset.events,
        "relations": relations,
        "chains": chains,
        "antichains": antichains,
    }