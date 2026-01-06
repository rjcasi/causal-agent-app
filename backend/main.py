from fastapi import FastAPI
from datetime import datetime

# Import the RMAT engine
from rmat_engine import RecursiveMatrixAttentionTensor

app = FastAPI()

# Create a single RMAT instance for the whole backend
rmat = RecursiveMatrixAttentionTensor(size=4)


# ---------------------------------------------------------
# BASIC HEALTH / HEARTBEAT ENDPOINTS
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/agent/heartbeat")
def agent_heartbeat():
    return {
        "alive": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/agent/status")
def agent_status():
    return {
        "heartbeat": True,
        "logs": [
            "Agent initialized",
            "RMAT engine online",
            "Awaiting tasks"
        ],
        "memory": {
            "short_term": [],
            "long_term": []
        },
        "modules": {
            "fuzzer": "idle",
            "defense": "ready",
            "symbolic_core": "initializing",
            "rmat": "active"
        }
    }


# ---------------------------------------------------------
# RMAT ORGAN ENDPOINTS
# ---------------------------------------------------------

@app.get("/agent/rmat/state")
def rmat_state():
    """
    Return the current RMAT state without advancing time.
    """
    return {"state": rmat.as_dict()}


@app.post("/agent/rmat/step")
def rmat_step(payload: dict | None = None):
    """
    Advance the RMAT engine one timestep.
    Optional: pass {"input": [...]} to drive spikes.
    """
    external_input = None

    if payload and "input" in payload:
        external_input = payload["input"]

    state = rmat.step(external_input=external_input)
    return {"state": rmat.as_dict()}


@app.get("/agent/rmat/view")
def rmat_view():
    """
    A simplified RMAT state for cockpit visualization.
    """
    s = rmat.state
    return {
        "timestep": s.timestep,
        "spikes": s.spikes,
        "density": s.density,
        "attention": s.attention,
        "phase_space": {
            "position": s.phase_space[: rmat.size],
            "momentum": s.phase_space[rmat.size:],
        }
    }