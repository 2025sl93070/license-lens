# LicenseLens

An explainable open-source license risk and dependency analysis tool.

LicenseLens helps developers analyze their project dependencies, identify associated licenses, evaluate them against configurable policies, and understand potential licensing risks in plain language.

## Features

- Analyze `package.json` (npm) and `requirements.txt` (Python) dependency files
- Identify licenses for direct and transitive dependencies
- Flag potentially risky licenses (GPL, Unknown, missing)
- Visualize dependency tree with license status
- Generate downloadable license reports

## Tech Stack

- **Frontend:** React.js, React Flow
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Testing:** Pytest
- **CI:** GitHub Actions

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting pull requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
