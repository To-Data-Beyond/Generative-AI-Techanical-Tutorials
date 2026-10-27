# Stable Diffusion Web App

A FastAPI backend and React/Chakra UI client using the original Stable Diffusion
v1-4 checkpoint, full 50-step generation and 256×256 output. The safety checker
stays enabled. No Hub token is required for this public checkpoint; its model
license still applies. CUDA uses float16; CPU and Apple MPS use float32. Apple
MPS uses attention slicing. The notebook runs real local HTTP requests and a
production client build; separate DOM tests mock only HTTP transport to test
client states, not model inference.

Use Python 3.11 and Node 22.12+ (or a supported newer Node release).

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

In a second terminal, from `client/`:

```bash
npm ci
npm run build
npm test
npm start
```

Open `http://127.0.0.1:5173`. The first request loads the model and can take
time. The backend allows only the two local port-5173 origins, validates prompt
and seed bounds, serializes inference with a lock, and returns actual PNG bytes.
The frontend uses query parameters, blob URLs, error recovery and URL cleanup.
This is a local educational app, not an authenticated public inference service.

The main notebook is [Stable_Diffusion_Web_App.ipynb](../../Stable_Diffusion_Web_App.ipynb).
Original source code is preserved in its nonexecuting appendix.
