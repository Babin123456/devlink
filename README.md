<p align="center">
  <img src="logo-dev.jpeg" alt="DevLink Banner" width="100%">
</p>

<h1 align="center">DevLink</h1>

<p align="center">
Open Source Developer Collaboration Platform
</p>

<p align="center">
Discover developers. Build teams. Ship software.
</p>

<p align="center">
  <a href="https://github.com/nensii21/devlink/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/nensii21/devlink/ci.yml?style=flat-square&label=build">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/github/license/nensii21/devlink?style=flat-square">
  </a>
  <a href="https://github.com/nensii21/devlink/stargazers">
    <img src="https://img.shields.io/github/stars/nensii21/devlink?style=flat-square">
  </a>
  <a href="https://github.com/nensii21/devlink/graphs/contributors">

    ## Overview

DevLink is an open-source collaboration platform built for developers, designers, founders, and open-source contributors.

It helps builders discover teammates, create projects, manage applications, collaborate in real time, and showcase their work in a single platform.

Whether you're building a startup, contributing to open source, or participating in hackathons, DevLink provides the tools to move from idea to production with the right people.

## Why DevLink

Building software often requires multiple disconnected tools.

| Platform | Purpose |
|----------|----------|
| GitHub | Source Code |
| LinkedIn | Professional Network |
| Discord | Communication |
| Notion | Documentation |
| Forms | Team Applications |

DevLink combines these workflows into one platform designed specifically for developers.

## Features

| Feature | Description |
|----------|-------------|
| Developer Profiles | Showcase skills, repositories, portfolio, and experience. |
| Project Marketplace | Discover projects or recruit contributors. |
| Team Applications | Apply to projects directly from the platform. |
| Real-Time Messaging | Collaborate instantly using WebSockets. |
| Notifications | Receive live updates across projects. |
| GitHub Integration | Link repositories and contribution history. |
| AI Recommendations | Discover teammates based on skills and interests. |
| Responsive Design | Optimized for desktop, tablet, and mobile. |

Architecture
graph LR

A[Browser]

B[React]

C[FastAPI]

D[Redis]

E[PostgreSQL]

A --> B

B --> C

C --> D

C --> E

## Architecture

DevLink follows a modern client-server architecture.

- React powers the frontend.
- FastAPI provides REST APIs and WebSocket communication.
- PostgreSQL stores application data.
- Redis enables caching and real-time messaging.

## Technology Stack

### Frontend

- React 19
- TypeScript
- Tailwind CSS
- TanStack Query
- TanStack Router
- Framer Motion

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- AsyncPG

### Infrastructure

- PostgreSQL
- Redis
- Docker
- GitHub Actions

Repository Structure
devlink/

├── backend/

├── frontend/

├── docs/

├── docker/

├── .github/

├── docker-compose.yml

└── README.md

Getting Started
git clone https://github.com/nensii21/devlink.git

cd devlink

cp .env.example .env

docker compose up --build

##Environment Variables

| Variable             | Description           |
| -------------------- | --------------------- |
| DATABASE_URL         | PostgreSQL connection |
| REDIS_URL            | Redis server          |
| SECRET_KEY           | JWT secret            |
| OPENAI_API_KEY       | AI features           |
| GITHUB_CLIENT_ID     | OAuth                 |
| GITHUB_CLIENT_SECRET | OAuth                 |

## API Documentation

| Endpoint | Description |
|----------|-------------|
| /api/auth | Authentication |
| /api/users | Users |
| /api/projects | Projects |
| /api/messages | Messaging |
| /api/applications | Applications |

Interactive documentation is available at

http://localhost:8000/docs

Testing
npm run test

npm run lint

npm run typecheck

pytest

## Deployment

DevLink can be deployed using Docker Compose for local development or containerized for cloud platforms such as Railway, Render, AWS, Google Cloud, and Azure.
    <img src="https://img.shields.io/github/contributors/nensii21/devlink?style=flat-square">
  </a>
</p>

Roadmap
| Version             | Status      |
| ------------------- | ----------- |
| Authentication      | Complete    |
| Project Marketplace | Complete    |
| Messaging           | Complete    |
| AI Recommendations  | In Progress |
| Organizations       | Planned     |
| Mobile Application  | Planned     |

## Contributing

We welcome contributions from developers of all experience levels.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Please read the CONTRIBUTING.md guide before submitting your PR.

## License

Licensed under the MIT License.

See the LICENSE file for more information.
