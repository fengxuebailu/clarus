# Quick Start Guide

## 5-Minute Setup

### 1. Clone & Configure

```bash
git clone https://github.com/fengxuebailu/clarus.git
cd clarus/backend
cp .env.example .env
```

Edit `backend/.env`:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Optional — without KataGo, the system uses mock data (demo mode)
KATAGO_PATH=/path/to/katago
KATAGO_CONFIG=/path/to/analysis_config.cfg
KATAGO_MODEL=/path/to/model.bin.gz

SECRET_KEY=your-secret-key-here
```

### 2. Install & Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Open the UI

Open `frontend/workspace-go.html` in your browser, or use:

```bash
cd ..  # back to project root
python -m http.server 3000
# Visit http://localhost:3000/frontend/workspace-go.html
```

### Or Use Docker

```bash
cp backend/.env.example backend/.env
# Edit backend/.env
docker compose up
# Visit http://localhost:3000/workspace-go.html
```

---

## Verify Installation

Visit `http://localhost:8000/api/go/health` — you should see:

```json
{
  "status": "healthy",
  "agents": {
    "grandmaster": "ready",
    "scribe": "ready",
    "arbiter": "ready",
    "delta_hunter": "ready"
  },
  "war_room": "operational"
}
```

## Test Analysis

1. Open `frontend/workspace-go.html`
2. Keep defaults (Move A: Q16, Move B: D4)
3. Click "Start Analysis"
4. Watch the real-time agent dialogue

> Without KataGo configured, results use mock data for demonstration.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `No module named 'fastapi'` | Activate venv: `source venv/bin/activate` then `pip install -r requirements.txt` |
| CORS error | Add your frontend URL to `CORS_ORIGINS` in `.env` |
| Gemini API error | Check API key is valid and has quota |
| Mock data only | Install [KataGo](KATAGO_SETUP.md) for real AI analysis |

---

## What's Next

- [KataGo Setup](KATAGO_SETUP.md) — Enable real Go AI analysis
- [API Docs](http://localhost:8000/api/docs) — Interactive API documentation
- [README](../README.md) — Full project overview
