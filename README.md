<p align="center">
  <img src="docs/screenshots/hero-banner.png" alt="DevLink Banner" width="100%" style="border-radius: 6px;">
</p>

<h1 align="center">DevLink</h1>

<p align="center">
  <strong>Open-Source Developer Collaboration & Teammate Discovery Engine</strong>
</p>

<p align="center">
  DevLink is an enterprise-grade developer collaboration platform designed to connect software engineers, open-source maintainers, UI/UX designers, and AI researchers. The system automates teammate discovery, manages project applications, scores repository quality, and facilitates real-time communication.
</p>

<p align="center">
  <a href="https://github.com/nensii21/devlink/actions"><img src="https://img.shields.io/github/actions/workflow/status/nensii21/devlink/ci.yml?branch=main&style=flat-square&label=build" alt="Build Status"></a>
  <a href="https://github.com/nensii21/devlink/releases"><img src="https://img.shields.io/github/v/release/nensii21/devlink?style=flat-square&color=green" alt="Release"></a>
  <a href="https://github.com/nensii21/devlink/blob/main/LICENSE"><img src="https://img.shields.io/github/license/nensii21/devlink?style=flat-square&color=blue" alt="License"></a>
  <a href="https://docker.com"><img src="https://img.shields.io/badge/docker-ready-blue?style=flat-square&logo=docker" alt="Docker"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square&logo=python" alt="Python"></a>
  <a href="https://react.dev"><img src="https://img.shields.io/badge/react-19.0-blue?style=flat-square&logo=react" alt="React"></a>
  <a href="https://fastapi.tiangolo.com"><img src="https://img.shields.io/badge/fastapi-0.110.0-green?style=flat-square&logo=fastapi" alt="FastAPI"></a>
  <a href="https://postgresql.org"><img src="https://img.shields.io/badge/postgresql-15.0%2B-blue?style=flat-square&logo=postgresql" alt="PostgreSQL"></a>
  <a href="https://redis.io"><img src="https://img.shields.io/badge/redis-7.0%2B-red?style=flat-square&logo=redis" alt="Redis"></a>
</p>

<p align="center">
  <a href="https://github.com/nensii21/devlink/stargazers"><img src="https://img.shields.io/github/stars/nensii21/devlink?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/nensii21/devlink/network/members"><img src="https://img.shields.io/github/forks/nensii21/devlink?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/nensii21/devlink/issues"><img src="https://img.shields.io/github/issues/nensii21/devlink?style=flat-square" alt="Issues"></a>
  <a href="https://github.com/nensii21/devlink/pulls"><img src="https://img.shields.io/github/issues-pr/nensii21/devlink?style=flat-square" alt="Pull Requests"></a>
  <a href="https://github.com/nensii21/devlink/graphs/contributors"><img src="https://img.shields.io/github/contributors/nensii21/devlink?style=flat-square" alt="Contributors"></a>
</p>

---

## Navigation

- [Project Status](#project-status)
- [Why DevLink?](#why-devlink)
- [Application Screenshots](#application-screenshots)
- [Feature Matrix](#feature-matrix)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Environment Variables](#environment-variables)
- [Development Scripts](#development-scripts)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Security](#security)
- [Performance](#performance)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## Project Status

| Property | Value |
| :--- | :--- |
| **Development Stage** | `v0.3.0-rc` (Release Candidate) |
| **API Version** | `v1.0.0` (`/api/v1`) |
| **Build Status** | `Passing` (GitHub Actions CI/CD) |
| **License** | MIT License |
| **Maintainer** | Nensi Patel ([@nensii21](https://github.com/nensii21)) |
| **Ecosystem** | ECSoc 2026 Open Source Project |

---

## Why DevLink?

Establishing high-performing software development teams is often hampered by fragmented communication across chat servers, unverified portfolio claims, and manual outreach. Traditional social networks lack technical context, while code-hosting platforms do not provide dedicated team matchmaking or application tracking.

DevLink provides a unified technical infrastructure that addresses these challenges:

- **Verified Technical Profiles**: Teammate recommendations evaluate actual GitHub repository statistics, commit frequency, code quality scores, and skill tags.
- **Structured Application Pipeline**: Project creators define explicit role requirements and tech stack criteria; candidates submit structured applications with verified credentials.
- **Integrated Real-Time Collaboration**: Native WebSocket direct messaging, activity feeds, saved search alerts, and notification channels streamline project initialization.

---

## Application Screenshots

### Dashboard
Real-time command center displaying active projects, match percentages, unread messages, and system recommendations.

![Dashboard](docs/screenshots/dashboard.png)

---

### Project Marketplace
Searchable repository of open-source projects and collaboration postings with technology filters and application status tracking.

![Projects Marketplace](docs/screenshots/projects.png)

---

### Real-Time Direct Messaging
Low-latency workspace messaging powered by WebSockets, featuring online presence and typing indicators.

![Messaging](docs/screenshots/messaging.png)

---

### Interface Views

| Authentication & OAuth 2.0 | Activity Feed & Flares | Mobile Responsive View |
| :---: | :---: | :---: |
| ![Login](docs/screenshots/login.png) | ![Feed](docs/screenshots/feed.png) | ![Mobile View](docs/screenshots/mobile.png) |
| *JWT & GitHub OAuth authentication* | *Community activity updates and flares* | *Optimized for mobile viewports* |

---

## Feature Matrix

| Domain | Capabilities | Core Components |
| :--- | :--- | :--- |
| **Developer Profiles** | Portfolio management, skill matrices, GitHub stats integration, social profile linking. | React 19, FastAPI, Pydantic, SQLAlchemy |
| **Project Marketplace** | Role postings, application submission tracking, applicant management, bookmark collections. | FastAPI, PostgreSQL, Asyncpg, TanStack Query |
| **Teammate Matchmaking** | AI-assisted compatibility calculations, skill overlap metrics, availability filters. | OpenAI API, NumPy, Pandas |
| **Real-Time Messaging** | Direct messaging (DM), presence management, typing indicators, notification events. | WebSockets, Redis Pub/Sub |
| **Repository Quality** | Automated quality scoring evaluating documentation completeness, coverage, and commit velocity. | GitHub REST/GraphQL API |
| **Search & Discovery** | Multi-entity full-text search across profiles, projects, issues, and skills with saved query alerts. | PostgreSQL Full-Text Search, Redis |

---

## System Architecture

DevLink follows a decoupled, service-oriented architecture designed for low-latency REST endpoints and scalable real-time event streaming.

```mermaid
graph TB
    subgraph Client Layer
        WebClient[Web Application Browser]
        MobileClient[Mobile Web Browser]
    end

    subgraph Gateway & Ingress
        ReverseProxy[Nginx Ingress / Reverse Proxy]
    end

    subgraph Presentation Server
        NodeServer[React 19 / Vite App Server]
    end

    subgraph Application API Layer
        FastAPI[FastAPI Application Server]
        AuthModule[JWT & OAuth Module]
        MatchEngine[AI Teammate Engine]
        WSManager[WebSocket Manager]
    end

    subgraph Storage & Processing
        CeleryWorker[Celery Task Workers]
        PostgreSQL[(PostgreSQL Relational DB)]
        Redis[(Redis Cache & Pub/Sub)]
        CloudStorage[Cloud Object Storage]
    end

    WebClient -->|HTTPS / WSS| ReverseProxy
    MobileClient -->|HTTPS / WSS| ReverseProxy
    ReverseProxy -->|Static Assets| NodeServer
    ReverseProxy -->|REST API & WS| FastAPI

    FastAPI --> AuthModule
    FastAPI --> MatchEngine
    FastAPI --> WSManager
    FastAPI --> PostgreSQL
    FastAPI --> Redis

    FastAPI --> CeleryWorker
    CeleryWorker --> PostgreSQL
    CeleryWorker --> Redis
    CeleryWorker --> CloudStorage
```

### Technical Design Rationale
- **Decoupled Architecture**: Complete separation of frontend presentation (React 19 SPA) and backend business logic (FastAPI REST API).
- **Stateless Authentication**: Cryptographically signed JWT tokens with short expiry periods and secure refresh token rotation.
- **Real-Time Messaging Engine**: Asynchronous WebSocket handlers scaled horizontally using Redis Pub/Sub channels.
- **Asynchronous Data Access**: Non-blocking database access via `asyncpg` and SQLAlchemy 2.0 async engine to optimize concurrent connection volume.

For complete architectural specifications, see [Architecture Documentation](docs/architecture.md).

---

## Tech Stack

| Tier | Technologies |
| :--- | :--- |
| **Frontend Framework** | React 19, TypeScript 5.8, Vite |
| **State & Routing** | TanStack Query v5, TanStack Router |
| **Styling** | Tailwind CSS v4, Framer Motion |
| **Backend API** | Python 3.11+, FastAPI, Pydantic v2 |
| **ORM & Database** | SQLAlchemy 2.0, Asyncpg, PostgreSQL 15+ |
| **Realtime & Caching** | WebSockets, Redis 7+ |
| **Task Queue** | Celery, Redis Broker |
| **DevOps & Containers** | Docker, Docker Compose, DevContainers, GitHub Actions |

---

## Repository Structure

```
devlink/
├── .devcontainer/           # VS Code & GitHub Codespaces configuration
│   ├── devcontainer.json
│   └── Dockerfile
├── .github/                 # Workflows, CI/CD pipelines, and templates
│   └── workflows/
├── backend/                 # FastAPI REST API & Async Services
│   ├── alembic/             # Database schema migration scripts
│   ├── app/
│   │   ├── core/            # Configuration, security, events, cache
│   │   ├── database/        # Async database session initialization
│   │   ├── middleware/      # Rate limiting, security headers, request ID
│   │   ├── models/          # SQLAlchemy ORM model definitions
│   │   ├── routers/         # REST API route handlers
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── services/        # Domain business logic & AI scoring services
│   │   └── main.py          # FastAPI application entrypoint
│   ├── tests/               # Pytest automated test suite
│   ├── Dockerfile.dev       # Backend development container file
│   └── requirements.txt     # Python package requirements
├── frontend/                # React 19 Frontend Web Application
│   ├── src/
│   │   ├── api/             # API HTTP client modules
│   │   ├── components/      # UI component library & layouts
│   │   ├── context/         # React state context providers
│   │   ├── hooks/           # Custom React hooks
│   │   └── routes/          # Application page routes
│   ├── Dockerfile.dev       # Frontend development container file
│   └── package.json         # Node.js dependencies and script manifests
├── docs/                    # System documentation and visual assets
│   ├── screenshots/         # Application interface screenshots
│   ├── api.md               # REST API documentation
│   ├── architecture.md      # System architecture & Mermaid diagrams
│   ├── coding-standards.md  # Code style and linting guidelines
│   ├── deployment.md        # Production deployment guide
│   └── development.md       # Local development setup guide
├── docker-compose.dev.yml   # Multi-service local development environment
├── CONTRIBUTING.md          # Open-source contribution guidelines
├── LICENSE                  # MIT License
└── README.md                # Project documentation
```

---

## Environment Variables

### Backend Configuration (`backend/.env`)

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `ENVIRONMENT` | Yes | `development` | Runtime environment (`development`, `staging`, `production`) |
| `DATABASE_URL` | Yes | `postgresql://postgres:postgres@localhost:5432/devlink_db` | Async PostgreSQL connection string |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Redis cache and message broker connection URI |
| `SECRET_KEY` | Yes | `dev_secret_key_change_in_production` | Secret key for JWT signature validation |
| `JWT_ALGORITHM` | No | `HS256` | Cryptographic algorithm for JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `1440` | Token expiration period in minutes |
| `GITHUB_CLIENT_ID` | No | `""` | GitHub OAuth Application Client ID |
| `GITHUB_CLIENT_SECRET` | No | `""` | GitHub OAuth Application Client Secret |
| `OPENAI_API_KEY` | No | `""` | OpenAI API key for matchmaking calculations |
| `CORS_ORIGINS` | No | `["http://localhost:5173"]` | Permitted CORS origins |

### Frontend Configuration (`frontend/.env`)

| Variable | Required | Default | Description |
| :--- | :---: | :--- | :--- |
| `VITE_API_URL` | Yes | `http://localhost:8000` | Backend API base endpoint URL |
| `VITE_APP_NAME` | No | `DevLink` | Platform title in header navigation |

---

## Development Scripts

### Frontend Scripts (`frontend/`)

| Script | Command | Action |
| :--- | :--- | :--- |
| `dev` | `npm run dev` | Starts Vite local development server with HMR |
| `build` | `npm run build` | Compiles production assets |
| `test` | `npm run test` | Runs unit tests via Vitest |
| `lint` | `npm run lint` | Executes ESLint static code analysis |
| `format` | `npm run format` | Formats codebase using Prettier |
| `typecheck` | `npm run typecheck` | Runs TypeScript compiler type checking without emitting files |

### Backend Scripts (`backend/`)

| Command | Action |
| :--- | :--- |
| `uvicorn app.main:app --reload` | Runs FastAPI server with hot-reloading |
| `pytest` | Runs Pytest test suite |
| `pytest --cov=app` | Executes test coverage analysis |
| `alembic upgrade head` | Applies pending database migrations |
| `alembic revision --autogenerate -m "message"` | Creates automated Alembic migration script |

---

## Deployment

### 1. Docker Compose (Recommended)
Launch the entire system (Frontend, Backend, PostgreSQL, and Redis) with a single command:

```bash
docker-compose -f docker-compose.dev.yml up --build
```

Endpoints:
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000/api`
- Swagger UI: `http://localhost:8000/docs`

### 2. DevContainers (VS Code & Codespaces)
This repository includes a `.devcontainer/` setup. Open the project folder in VS Code and execute **Remote-Containers: Reopen in Container** or launch in GitHub Codespaces. Dependencies, database CLI tools, and port forwarding are configured automatically.

### 3. Cloud Deployment
- **Frontend**: Deploy `frontend/` as a static build to Vercel, Netlify, or Cloudflare Pages.
- **Backend**: Containerize using `backend/Dockerfile` and deploy to Render, Railway, AWS ECS, or Google Cloud Run.
- **Databases**: Use managed services like AWS RDS (PostgreSQL) and Upstash / AWS ElastiCache (Redis).

For full deployment documentation, see [Deployment Guide](docs/deployment.md).

---

## API Documentation

DevLink provides full REST API documentation. Interactive Swagger UI is generated automatically when running the backend:

- **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Technical Reference**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Schema Specification**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

For detailed endpoint documentation, see [API Reference](docs/api.md).

---

## Testing

Automated test suites ensure code quality and prevent regression issues.

### Running Backend Tests
```bash
cd backend
pytest -v
```

### Running Frontend Tests
```bash
cd frontend
npm run test
npm run typecheck
```

---

## Security

Security practices implemented across the platform:

- **Authentication & OAuth**: Bcrypt password hashing, JWT token rotation, state verification on GitHub OAuth.
- **Rate Limiting**: `SlowAPI` middleware limits request frequency to protect against Denial-of-Service attacks.
- **Security Headers**: Enforced HTTP headers via `SecurityHeadersMiddleware` (CSP, HSTS, X-Frame-Options, X-Content-Type-Options).
- **Data Validation**: Strict Pydantic v2 request body validation and parameterized SQL queries via SQLAlchemy to prevent SQL injection.

For security reports, view [Security Policy](SECURITY.md).

---

## Performance

- **Database Connection Pooling**: SQLAlchemy async engines utilize connection pooling for high concurrent query throughput.
- **Redis Caching**: Cached database lookups for user profiles, search queries, and repository scores reduce database load.
- **Frontend Optimization**: Code splitting, dynamic imports, and asset optimization via Vite deliver sub-100ms load times.

---

## Roadmap

```
v0.1.0 (Alpha)           v0.2.0 (Beta)            v0.3.0 (RC - Current)    v1.0.0 (GA - Planned)
├── Core Auth            ├── WebSockets DM        ├── AI Teammate Matching ├── Mobile App (React Native)
├── User Profiles        ├── Application Engine   ├── Profile Summarizer   ├── Organization Workspaces
└── Project Postings     └── Repo Quality Scoring └── Builder Flares Feed   └── Public Developer API
```

### Milestone Breakdown
- **v0.1.0 (Alpha - Core Engine)**: User authentication, JWT tokens, profile management, and project marketplace postings. *(Completed)*
- **v0.2.0 (Beta - Realtime Features)**: WebSocket direct messaging, live notifications, project application engine, and repository quality scoring. *(Completed)*
- **v0.3.0 (RC - AI & Analytics)**: Teammate matching algorithms, profile summarization, saved search alerts, and builder activity flares. *(Current Release)*
- **v1.0.0 (GA - Enterprise Scale)**: React Native mobile application, organization team workspaces, enterprise SSO/SAML, and public REST API. *(Planned)*

---

## Contributing

Contributions from the developer community are welcome.

1. Fork the repository on GitHub.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit changes adhering to [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m "feat(auth): add OAuth provider"`
4. Push to origin: `git push origin feature/your-feature-name`
5. Open a Pull Request pointing to `main`.

Please review [Contribution Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before submitting pull requests.

---

## License

DevLink is open-source software licensed under the **MIT License**. See [LICENSE](LICENSE) for details.
