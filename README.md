# MABOS - Multi-Agent Business Operating System

## Project Overview

MABOS is the first enterprise-grade Multi-Agent Business Operating System that seamlessly combines theoretical BDI (Belief-Desire-Intention) architecture with practical workflow orchestration, delivering intelligent, adaptive business automation at scale.

### 🚀 Key Features

- **BDI Agent Engine**: Sophisticated belief-desire-intention reasoning system
- **Conversational Workflow Builder**: Natural language workflow creation
- **Visual Workflow Designer**: Drag-and-drop interface with real-time collaboration
- **Enterprise Integrations**: Native connectors for SAP, Salesforce, ServiceNow, Microsoft 365, Oracle
- **LLM Gateway**: Multi-provider integration with intelligent routing and caching
- **Zero-Trust Security**: Comprehensive security compliance (SOC 2, GDPR, WCAG 2.1 AA)

### 🏗️ Architecture

```
MABOS/
├── frontend/          # Next.js 14+ React application
├── backend/           # Python FastAPI microservices
├── shared/            # Shared types and utilities
├── docs/              # Documentation and specifications
├── scripts/           # Development and deployment scripts
├── tests/             # Cross-service integration tests
└── infrastructure/    # Kubernetes and deployment configs
```

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14+ with React 18.3+ and TypeScript 5.4+
- **UI Components**: Radix UI + Tailwind CSS
- **State Management**: Zustand + TanStack Query
- **Workflow Designer**: React Flow/XyFlow
- **Testing**: Jest + Playwright + Storybook

### Backend
- **Framework**: Python 3.11+ with FastAPI 0.110+
- **BDI Engine**: Owlready2 + NetworkX + Neo4j
- **Databases**: PostgreSQL + Redis + Elasticsearch
- **LLM Integration**: LiteLLM with multi-provider support
- **Workflow Engine**: Celery + YAML definitions
- **Testing**: pytest + Locust + OWASP ZAP

## 📋 Prerequisites

- **Node.js**: 18.17+ or 20.5+
- **Python**: 3.11+
- **Docker**: 24.0+
- **Docker Compose**: 2.20+
- **Kubernetes**: 1.28+ (for production)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/mabos/mabos-workbench.git
cd mabos-workbench

# Install dependencies for both frontend and backend
npm run install:all

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 2. Development Environment

```bash
# Start all services with Docker Compose
docker-compose up -d

# Start frontend development server
npm run dev:frontend

# Start backend development server
npm run dev:backend
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Storybook**: http://localhost:6006

## 📁 Project Structure

```
mabos-workbench/
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/                # Next.js App Router
│   │   ├── components/         # React components
│   │   ├── lib/               # Utilities and API clients
│   │   ├── stores/            # Zustand state stores
│   │   └── types/             # TypeScript definitions
│   ├── public/                # Static assets
│   ├── tests/                 # Frontend tests
│   └── package.json
├── backend/                     # Python FastAPI services
│   ├── app/
│   │   ├── core/              # BDI engine and framework
│   │   ├── api/               # FastAPI routes
│   │   ├── services/          # Business logic
│   │   ├── models/            # Database models
│   │   ├── integrations/      # Enterprise connectors
│   │   └── tests/             # Backend tests
│   ├── migrations/            # Database migrations
│   ├── requirements.txt       # Python dependencies
│   └── pyproject.toml
├── shared/                      # Shared code and types
│   ├── types/                 # Common TypeScript types
│   └── utils/                 # Shared utilities
├── tests/                       # Integration and E2E tests
│   ├── integration/           # Cross-service tests
│   ├── e2e/                   # End-to-end tests
│   ├── performance/           # Load and performance tests
│   └── security/              # Security and penetration tests
├── docs/                        # Documentation
│   ├── api/                   # API documentation
│   ├── specs/                 # Technical specifications
│   └── guides/                # User and developer guides
├── scripts/                     # Development and deployment scripts
│   ├── setup/                 # Environment setup scripts
│   ├── build/                 # Build scripts
│   └── deploy/                # Deployment scripts
├── infrastructure/              # Infrastructure as Code
│   ├── docker/                # Docker configurations
│   ├── kubernetes/            # K8s manifests
│   └── terraform/             # Terraform configurations
├── .github/                     # GitHub workflows
│   └── workflows/             # CI/CD pipelines
├── package.json                # Root package.json (monorepo)
├── docker-compose.yml          # Local development services
└── README.md
```

## 🧪 Testing Strategy

MABOS implements comprehensive testing following industry best practices:

### Unit Testing (90%+ Coverage)
```bash
# Frontend unit tests
npm run test:frontend

# Backend unit tests
npm run test:backend

# Coverage reports
npm run test:coverage
```

### Integration Testing
```bash
# API integration tests
npm run test:integration

# Database integration tests
npm run test:db

# External service integration tests
npm run test:integrations
```

### Performance Testing
```bash
# Load testing with K6
npm run test:load

# Stress testing
npm run test:stress

# Performance profiling
npm run test:performance
```

### Security Testing
```bash
# Security scanning
npm run test:security

# Vulnerability assessment
npm run test:vulnerabilities

# Penetration testing
npm run test:pentest
```

### End-to-End Testing
```bash
# E2E tests with Playwright
npm run test:e2e

# Visual regression testing
npm run test:visual

# Cross-browser testing
npm run test:browsers
```

## 🔧 Development

### Code Quality
```bash
# Linting
npm run lint

# Type checking
npm run type-check

# Code formatting
npm run format

# Pre-commit hooks
npm run pre-commit
```

### Database Management
```bash
# Run migrations
npm run db:migrate

# Seed database
npm run db:seed

# Reset database
npm run db:reset
```

### API Development
```bash
# Generate API client
npm run api:generate

# Validate OpenAPI schema
npm run api:validate

# Test API endpoints
npm run api:test
```

## 🚀 Deployment

### Development
```bash
# Deploy to development environment
npm run deploy:dev
```

### Staging
```bash
# Deploy to staging environment
npm run deploy:staging
```

### Production
```bash
# Deploy to production environment
npm run deploy:prod
```

## 📊 Monitoring

- **Application Performance**: Sentry error tracking and performance monitoring
- **Infrastructure**: Prometheus metrics and Grafana dashboards
- **Logging**: Structured logging with Elasticsearch and Kibana
- **Security**: Real-time security monitoring and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Guidelines

- Follow TypeScript/Python coding standards
- Write comprehensive tests (minimum 90% coverage)
- Update documentation for new features
- Run all tests before submitting PR
- Follow conventional commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.mabos.ai](https://docs.mabos.ai)
- **Issues**: [GitHub Issues](https://github.com/mabos/mabos-workbench/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mabos/mabos-workbench/discussions)
- **Email**: dev@mabos.ai

## 🗺️ Roadmap

- [ ] **Phase 1**: Core BDI Engine and Basic Workflow Designer
- [ ] **Phase 2**: Enterprise Integrations and LLM Gateway
- [ ] **Phase 3**: Advanced Analytics and Mobile App
- [ ] **Phase 4**: AI/ML Optimization and Global Localization

---

**MABOS** - Transforming Business Automation with Intelligent Multi-Agent Systems
