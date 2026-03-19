# Contributing to Clarus

Thanks for your interest in contributing! Whether you're a Go player, AI researcher, or developer — we'd love your help.

## Getting Started

1. Fork the repo
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/clarus.git`
3. Set up the backend (see [Quick Start](docs/QUICKSTART.md))
4. Create a branch: `git checkout -b feature/your-feature`

## What Can You Contribute?

### For Go Players
- Improve explanation quality and Go terminology
- Test analysis outputs for accuracy
- Add example positions and teaching scenarios

### For AI/ML Researchers
- Improve the prediction-verification loop
- Experiment with different LLM prompts
- Extend the framework to other domains

### For Developers
- Frontend improvements and new visualizations
- API enhancements
- Performance optimization
- Bug fixes

## Development Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python -m uvicorn app.main:app --reload
```

## Pull Request Process

1. Update documentation if you change any APIs
2. Test your changes locally
3. Write a clear PR description explaining what and why
4. Link any related issues

## Code Style

- Python: Follow PEP 8
- Frontend: Keep it simple — vanilla HTML/CSS/JS
- Commits: Use clear, descriptive messages

## Reporting Bugs

Open an issue with:
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)

## Questions?

Open a Discussion or Issue — we're happy to help!
