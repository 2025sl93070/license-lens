# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-27

### Added
- FastAPI backend with SQLAlchemy and SQLite database
- Dependency parser for `package.json` (npm) and `requirements.txt` (Python)
- Multi-source license resolution: PyPI, GitHub API, Repology, local fallback
- License policy engine with configurable policies (Enterprise Safe, Permissive Only, Copyleft Allowed)
- React 18 + TypeScript + Vite frontend
- Interactive dependency graph using React Flow
- Dependency table with risk badges
- Compare two projects side by side
- Analysis history page
- License glossary page
- Risk summary chart using Recharts
- Conflict detection panel
- Docker and Docker Compose support
- GitHub Actions CI/CD pipeline
- Pytest unit tests for parser and policy engine
