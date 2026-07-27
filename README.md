# <p align="center">DevLink</p>

<p align="center">
  <img src="docs/assets/banner.png" alt="DevLink Banner" width="100%">
</p>

<p align="center">
  <strong>The Open Source Platform for Developer Collaboration</strong>
</p>

<p align="center">
Connect with developers, discover projects, recruit teammates, collaborate in real time, and build production-ready software from one unified platform.
</p>

<p align="center">

[![License](https://img.shields.io/github/license/nensii21/devlink?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/nensii21/devlink?style=for-the-badge)](https://github.com/nensii21/devlink/stargazers)
[![Forks](https://img.shields.io/github/forks/nensii21/devlink?style=for-the-badge)](https://github.com/nensii21/devlink/network/members)
[![Issues](https://img.shields.io/github/issues/nensii21/devlink?style=for-the-badge)](https://github.com/nensii21/devlink/issues)
[![Pull Requests](https://img.shields.io/github/issues-pr/nensii21/devlink?style=for-the-badge)](https://github.com/nensii21/devlink/pulls)
[![Contributors](https://img.shields.io/github/contributors/nensii21/devlink?style=for-the-badge)](https://github.com/nensii21/devlink/graphs/contributors)
[![React](https://img.shields.io/badge/React-19-149ECA?style=for-the-badge\&logo=react\&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)]()
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge\&logo=typescript\&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)]()

</p>

---

# Overview

DevLink is an enterprise-grade open-source collaboration platform built for developers, founders, designers, AI engineers, and open-source contributors.

Instead of managing discussions across multiple platforms, DevLink centralizes developer networking, project recruitment, messaging, issue tracking, and collaboration into a single modern workspace.

Whether you're building a startup, preparing for a hackathon, or contributing to open source, DevLink helps you find the right people and ship faster.

---

# Why DevLink?

Modern software development is collaborative, but existing platforms solve only part of the problem.

GitHub manages code.

LinkedIn manages networking.

Discord manages communication.

Notion manages documentation.

DevLink brings everything together in one platform.

---

# Product Preview

<p align="center">
<img src="docs/images/dashboard.png" width="95%">
</p>

---

# Platform Screenshots

| Dashboard                                  | Authentication                         |
| ------------------------------------------ | -------------------------------------- |
| <img src="docs/screenshots/dashboard.png"> | <img src="docs/screenshots/login.png"> |

| Projects                                  | Feed                                  |
| ----------------------------------------- | ------------------------------------- |
| <img src="docs/screenshots/projects.png"> | <img src="docs/screenshots/feed.png"> |

| Mobile View                             | Messaging                             |
| --------------------------------------- | ------------------------------------- |
| <img src="docs/screenshots/mobile.png"> | <img src="docs/screenshots/chat.png"> |

---

# Features

| Feature              | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| Developer Profiles   | Showcase skills, repositories, experience, and availability |
| Project Marketplace  | Create projects and recruit contributors                    |
| AI Matchmaking       | Smart teammate recommendations                              |
| Repository Insights  | GitHub repository analysis                                  |
| Real-Time Messaging  | WebSocket powered chat                                      |
| Team Applications    | Review and manage applicants                                |
| Notifications        | Live project activity updates                               |
| Authentication       | JWT + GitHub OAuth                                          |
| Organization Support | Team collaboration                                          |
| Search               | Global developer and project search                         |

---

# Architecture

```text
                    Browser

                       │

             React + TypeScript

                       │

                REST / WebSocket

                       │

                  FastAPI API

          ┌──────────┴──────────┐

     Authentication      AI Matching

          │                    │

     PostgreSQL          Redis Cache

          │

    Background Workers
```

Detailed diagrams are available in

```
docs/architecture.md
```

---

# Technology Stack

| Category         | Technologies                          |
| ---------------- | ------------------------------------- |
| Frontend         | React 19, TypeScript, Tailwind CSS v4 |
| State Management | TanStack Query                        |
| Routing          | TanStack Router                       |
| Backend          | FastAPI                               |
| ORM              | SQLAlchemy 2                          |
| Validation       | Pydantic v2                           |
| Database         | PostgreSQL                            |
| Cache            | Redis                                 |
| Authentication   | JWT, OAuth 2.0                        |
| AI               | OpenAI API                            |
| Containers       | Docker                                |
| CI/CD            | GitHub Actions                        |

---

# Repository Structure

```text
devlink/

├── backend/
│   ├── app/
│   ├── tests/
│   └── migrations/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── components/
│
├── docs/
│
├── docker/
│
├── .github/
│
├── docker-compose.yml
│
└── README.md
```

---

# Quick Start

## Clone Repository

```bash
git clone https://github.com/nensii21/devlink.git

cd devlink
```

---

# Docker Installation

```bash
docker compose up --build
```

Services

| Service  | URL                        |
| -------- | -------------------------- |
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000      |
| API Docs | http://localhost:8000/docs |

---

# Local Development

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Environment Variables

Backend

```env
DATABASE_URL=

REDIS_URL=

JWT_SECRET=

OPENAI_API_KEY=

GITHUB_CLIENT_ID=

GITHUB_CLIENT_SECRET=
```

Frontend

```env
VITE_API_URL=

VITE_APP_NAME=
```

---

# API

| Module         | Endpoint           |
| -------------- | ------------------ |
| Authentication | /api/auth          |
| Users          | /api/users         |
| Projects       | /api/projects      |
| Applications   | /api/applications  |
| Messaging      | /api/messages      |
| Notifications  | /api/notifications |

Swagger

```
http://localhost:8000/docs
```

---

# Security

* JWT Authentication
* OAuth 2.0
* Password Hashing
* Refresh Tokens
* Secure HTTP Headers
* Input Validation
* SQL Injection Protection
* Rate Limiting
* CORS Protection
* XSS Protection

---

# Testing

Backend

```bash
pytest
```

Coverage

```bash
pytest --cov
```

Frontend

```bash
npm run test
```

Lint

```bash
npm run lint
```

---

# Performance

* Async FastAPI
* Redis Caching
* Lazy Loading
* Optimized API Responses
* WebSocket Communication
* Background Tasks
* Database Connection Pooling

---

# Documentation

| Guide        | Link                 |
| ------------ | -------------------- |
| API          | docs/api.md          |
| Architecture | docs/architecture.md |
| Development  | docs/development.md  |
| Contributing | CONTRIBUTING.md      |

---

# Roadmap

| Version | Status                    |
| ------- | ------------------------- |
| v0.8    | Authentication & Profiles |
| v0.9    | Messaging                 |
| v1.0    | AI Matchmaking            |
| v1.1    | Organizations             |
| v2.0    | Mobile Applications       |

---

# Contributing

1. Fork the repository.
2. Create a feature branch.
3. Follow Conventional Commits.
4. Submit a Pull Request.
5. Wait for review.

See **CONTRIBUTING.md** for complete contribution guidelines.

---

# License

Distributed under the MIT License.

See the LICENSE file for more information.

---

# Maintainers

**Lead Maintainer**

Nensi Patel

GitHub

https://github.com/nensii21

---

# Community

* Open Source Contributors
* GitHub Discussions
* Issues
* Pull Requests

---

<p align="center">

Built with React, FastAPI, PostgreSQL, Redis, and OpenAI.

Designed for developers who build together.

</p>
