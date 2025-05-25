# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

MABOS is a Multi-Agent Business Operating System that combines BDI (Belief-Desire-Intention) architecture with practical workflow orchestration. The project follows a monorepo structure with separate frontend and backend applications:

- **Frontend**: Next.js 14+ with React 18.3+ and TypeScript 5.4+
- **Backend**: Python 3.11+ with FastAPI 0.110+
- **Shared**: Common types and utilities
- **Infrastructure**: Docker, Kubernetes, and deployment configurations

## Essential Commands

### Development
```bash
# Start all services
npm run dev

# Individual services
npm run dev:frontend    # Next.js dev server at :3000
npm run dev:backend     # FastAPI server at :8000

# Full setup
npm run setup          # Install deps + migrate + seed DB
```

### Testing
```bash
# All tests
npm run test

# Specific test suites
npm run test:frontend
npm run test:backend
npm run test:integration
npm run test:e2e       # Playwright tests
```

### Code Quality
```bash
npm run lint           # ESLint + Flake8 + MyPy
npm run format         # Prettier + Black + isort  
npm run type-check     # TypeScript + MyPy
npm run pre-commit     # Full quality check
```

### Database Operations
```bash
npm run db:migrate     # Run Alembic migrations
npm run db:seed        # Populate with test data
npm run db:reset       # Drop, migrate, and seed
```

## Task Management System

This project uses a sophisticated task management system via `scripts/dev.js` or the global `task-master` CLI:

### Core Workflow
1. **Start sessions**: `task-master list` to see current tasks
2. **Find next task**: `task-master next` (respects dependencies)
3. **View task details**: `task-master show <id>`
4. **Break down complex tasks**: `task-master expand --id=<id> --research`
5. **Mark completed**: `task-master set-status --id=<id> --status=done`

### Key Task Commands
```bash
task-master analyze-complexity --research  # AI-powered task analysis
task-master expand --id=3 --research      # Generate subtasks with AI
task-master update --from=4 --prompt="..."  # Update future tasks
task-master fix-dependencies               # Clean up broken deps
```

### Task Structure
Tasks are stored in `tasks.json` with dependencies, priorities, and detailed implementation notes. The system automatically tracks prerequisite completion and suggests the optimal next task to work on.

## Important File Locations

- `tasks.json` - Master task list with dependencies
- `tasks/` - Individual task files with implementation details
- `scripts/task-complexity-report.json` - AI-generated complexity analysis
- `.windsurfrules` - Development workflow and coding standards
- `docs/specs/` - Technical specifications and requirements
- `package.json` - Monorepo scripts and workspace configuration

## Development Philosophy

- **Task-driven development**: All work should be tracked through the task management system
- **Dependency-aware**: Respect task dependencies and complete prerequisites first
- **AI-assisted planning**: Use complexity analysis and research-backed subtask generation
- **Quality-first**: Run linting, type checking, and tests before marking tasks complete

## Technology Stack Context

- **BDI Engine**: Sophisticated agent reasoning with Owlready2 + NetworkX + Neo4j
- **LLM Integration**: Multi-provider support via LiteLLM
- **UI Framework**: Radix UI + Tailwind CSS with React Flow for workflow designer
- **State Management**: Zustand + TanStack Query
- **Testing**: Jest + Playwright + pytest with 90%+ coverage requirement