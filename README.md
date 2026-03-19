<p align="center">
  <img src="assets/mascot/arctic-fox-sitting-v1.png" alt="Clarus" width="180" />
</p>

<h1 align="center">Clarus</h1>

<p align="center">
  <strong>Making Superhuman AI Transparent — Starting with Go/Weiqi</strong>
</p>

<p align="center">
  <a href="#features">Features</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue?logo=python&logoColor=white" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/KataGo-v1.16-green" alt="KataGo" />
  <img src="https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google&logoColor=white" alt="Gemini" />
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="License" />
</p>

---

## Why Clarus?

Superhuman AI systems like AlphaGo and KataGo can beat every human — but **nobody can explain why they make the moves they do**. Their decision logic is a black box.

**Clarus** cracks open that black box. It uses a multi-agent debate system to translate KataGo's raw mathematical outputs into **human-understandable reasoning** — and then **validates** that the explanation is actually correct through a novel prediction-based verification loop.

> *"If a student AI can read the explanation and find the right move on the board, the explanation works. If not, it gets rewritten."*

This is not just a Go app. It's a prototype for **Explainable AI (XAI)** that could extend to any domain where superhuman AI makes opaque decisions — medicine, finance, autonomous systems.

---

## Features

- **Multi-Agent Debate Engine** — 5 specialized AI agents collaborate and challenge each other to produce verified explanations
- **Prediction-Based Verification** — Explanations are tested: can a student AI find the right move just by reading the principle?
- **Real-Time Analysis** — WebSocket-powered live analysis with KataGo integration
- **Contrastive Learning** — Explains *why* move A is better than move B, not just what each move does
- **Interactive Go Board** — Play, analyze, and learn with a beautiful UI featuring an arctic fox mascot
- **Concept Feedback Loop** — When the student AI fails, it explains *what it misunderstood*, and the teacher rewrites the explanation

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Clarus War Room                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │ Grandmaster   │    │ Delta Hunter │    │   Scribe     │  │
│  │ (KataGo)     │───▶│ (Analyzer)   │───▶│ (Gemini LLM) │  │
│  │              │    │              │    │              │  │
│  │ Ground Truth │    │  ΔV = V_A -  │    │  Generates   │  │
│  │ V_A, V_B     │    │       V_B    │    │  Explanation  │  │
│  └──────────────┘    └──────────────┘    └──────┬───────┘  │
│                                                  │          │
│                                          ┌───────▼───────┐  │
│                                          │   Arbiter     │  │
│                                          │ (Student AI)  │  │
│                                          │               │  │
│                                          │ Can it find   │  │
│                                          │ the right     │  │
│                                          │ move?         │  │
│                                          └───────┬───────┘  │
│                                                  │          │
│                                          ┌───────▼───────┐  │
│                                          │  Validated?   │  │
│                                          │  ✓ Publish    │  │
│                                          │  ✗ Feedback   │──┘
│                                          │    & Retry    │
│                                          └───────────────┘
└─────────────────────────────────────────────────────────────┘
```

### The Agents

| Agent | Role | Backbone | What It Does |
|-------|------|----------|-------------|
| **Grandmaster** | Oracle | KataGo Engine | Generates ground truth: winrate, territory ownership, best moves |
| **Delta Hunter** | Analyst | Python | Computes what changed between two moves (ΔV) |
| **Scribe** | Teacher | Gemini LLM | Writes human-readable explanations using `Context → Action → Logic` |
| **Arbiter** | Student | Gemini LLM | Reads the explanation blind and tries to predict the correct move |

### Verification Loop

```
Scribe writes explanation
    → Arbiter reads it and guesses the move
        → Correct? Ship it ✓
        → Wrong? Arbiter explains what it misunderstood
            → Scribe rewrites with better terminology
                → Retry (max 3 rounds)
```

---

## Quick Start

### Prerequisites

- Python 3.9+
- [KataGo](https://github.com/lightvector/KataGo) (local install)
- [Google Gemini API key](https://aistudio.google.com/apikey)

### Setup

```bash
# Clone
git clone https://github.com/fengxuebailu/clarus.git
cd clarus

# Backend setup
cd backend
cp .env.example .env
# Edit .env with your Gemini API key and KataGo path

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Open the UI

Open `workspace-go.html` in your browser, or visit `http://localhost:8000/api/docs` for the API documentation.

---

## How It Works

### 1. Position Analysis

Send a board position with two candidate moves. KataGo evaluates both in parallel, producing mathematical ground truth vectors (winrate, score lead, territory ownership for every intersection).

### 2. Delta Extraction

The Delta Hunter compares the two vectors and identifies what changed — which territories shifted, how much winrate swung, what tactical patterns emerged.

### 3. Explanation Generation

The Scribe (powered by Gemini) translates these mathematical deltas into a structured explanation following the **Context → Action → Logic** formula:

> *"In a double-atari position, when both groups have 3 liberties, you must extend rather than capture the ko. Extending preserves connection to the living group. Mathematical consequence: liberties 4 vs 2 = you survive."*

### 4. Prediction Verification

The Arbiter (a separate LLM instance acting as a student) reads *only* the abstract principle — no coordinates, no board position — and tries to predict which move is correct.

- **If correct**: The explanation genuinely conveys the tactical insight
- **If wrong**: The Arbiter explains its confusion ("I interpreted 'press' as attack, but it meant 'connect'"), and the Scribe rewrites

---

## Project Structure

```
clarus/
├── backend/
│   ├── app/
│   │   ├── agents/           # AI Agent implementations
│   │   │   ├── grandmaster.py    # KataGo interface
│   │   │   ├── scribe.py         # LLM explanation generator
│   │   │   ├── arbiter.py        # Prediction verifier
│   │   │   ├── delta_hunter.py   # Difference analyzer
│   │   │   └── prompts.py        # System prompts
│   │   ├── seminars/
│   │   │   └── war_room.py       # Orchestration engine
│   │   ├── api/
│   │   │   ├── routes.py         # REST endpoints
│   │   │   └── websocket_routes.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── katago_client.py
│   │   └── main.py
│   └── requirements.txt
├── workspace-go.html         # Main workspace UI
├── go-demo.html              # Interactive Go board
├── insight-library.html      # Knowledge base
├── assets/mascot/            # Arctic fox mascot 🦊
└── README.md
```

---

## API

### REST Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/go/analyze` | Analyze a position with two candidate moves |
| `POST` | `/api/go/analyze/batch` | Batch analysis of multiple positions |
| `GET`  | `/api/go/health` | Health check (includes KataGo status) |
| `GET`  | `/api/go/concepts` | List available Go concepts |

### WebSocket

Connect to `/api/ws/analyze` for real-time streaming analysis with live agent dialogue.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Python 3.9+ |
| Go Engine | KataGo v1.16 (local, CPU/GPU) |
| LLM | Google Gemini 2.5 Flash |
| Frontend | Vanilla HTML/CSS/JS |
| Real-time | WebSocket |

---

## Roadmap

- [ ] SGF file import/export
- [ ] Game review mode (full-game analysis)
- [ ] User accounts & progress tracking
- [ ] Seminar II: Strategy Room (macro-level whole-board analysis)
- [ ] Multi-language explanation support
- [ ] Extend the verification framework beyond Go

---

## The Bigger Picture

Go is just the beginning. The core innovation — **using prediction-based verification to ensure AI explanations are actually useful** — applies anywhere superhuman AI makes decisions:

- **Medical AI**: Can a doctor, reading only the explanation, arrive at the same diagnosis?
- **Trading AI**: Can an analyst, reading the rationale, predict the same position?
- **Autonomous Systems**: Can an engineer, reading the decision log, predict the system's action?

If the explanation passes the prediction test, it works. If not, rewrite it until it does.

---

## Contributing

Contributions are welcome! Whether you're a Go player, an AI researcher, or a developer interested in explainable AI:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<p align="center">
  <img src="assets/mascot/arctic-fox-waving.png" alt="Clarus Fox" width="100" />
  <br />
  <em>Built with curiosity by the Clarus team</em>
</p>
