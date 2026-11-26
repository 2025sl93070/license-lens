# LicenseLens

An explainable open-source license risk and dependency analysis tool.

LicenseLens helps developers analyze their project dependencies, identify associated licenses, evaluate them against configurable policies, and understand potential licensing risks in plain language.

## Features

- Analyze `package.json` (npm) and `requirements.txt` (Python) dependency files
- Identify licenses for direct and transitive dependencies via PyPI, GitHub API, and Repology
- Flag potentially risky licenses (GPL, AGPL, Unknown)
- Visualize dependency tree with license status using an interactive graph
- Compare two projects side by side
- View analysis history
- Browse license glossary
- Generate downloadable license reports
- Configurable license policies (Enterprise Safe, Permissive Only, Copyleft Allowed)

## Tech Stack

- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, React Flow, TanStack Query, Recharts
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, SQLite, Alembic
- **Testing:** Pytest, pytest-asyncio
- **CI/CD:** GitHub Actions
- **Containerization:** Docker, Docker Compose

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend Setup

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Run with Docker

```bash
docker-compose up --build
```

Frontend: http://localhost:3000  
Backend API: http://localhost:8000  
API Docs: http://localhost:8000/docs

## Project Structure

```
license-lens/
├── backend/
│   ├── app/
│   │   ├── data/          # License database and sample data
│   │   ├── parsers/       # npm and Python dependency parsers
│   │   ├── routers/       # FastAPI route handlers
│   │   └── services/      # Business logic
│   └── tests/
├── frontend/
│   └── src/
│       ├── components/    # Reusable UI components
│       ├── pages/         # Page components
│       ├── types/         # TypeScript type definitions
│       └── lib/           # API client and utilities
└── docker-compose.yml
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
