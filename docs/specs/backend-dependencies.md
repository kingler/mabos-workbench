# MABOS Backend Dependencies Specification

## Core Framework & Architecture

Based on the reference codebases (Dify_MABOS, MABOS-Standalone, and Suna), we'll use **Python 3.11+** with **FastAPI** for high-performance API development and comprehensive BDI agent implementation.

## Core Dependencies (requirements.txt)

```python
# ===== Core Framework =====
# FastAPI for high-performance API (like Dify_MABOS and Suna)
fastapi==0.110.0
uvicorn[standard]==0.27.0
gunicorn==21.2.0

# ===== ASGI & HTTP =====
httpx==0.27.0
aiohttp==3.9.0
starlette==0.36.0

# ===== BDI Agent Framework (from MABOS-Standalone and Dify_MABOS) =====
# Ontology Management (like Dify_MABOS)
owlready2==0.46
rdflib==7.0.0
sparqlwrapper==2.0.0

# Knowledge Graph Management (like MABOS-Standalone)
networkx==3.2.1
neo4j==5.17.0
py2neo==2021.2.4

# Reasoning and Logic
pyke==1.1.1
pyDatalog==0.17.1

# ===== AI/ML Integration =====
# LLM Providers (comprehensive support like reference codebases)
openai==1.12.0
anthropic==0.18.0
google-generativeai==0.4.0
litellm==1.31.0
langchain==0.1.10
langchain-core==0.1.25
langchain-community==0.0.25
transformers==4.38.0
torch==2.2.0
sentence-transformers==2.4.0

# ===== Database & Storage =====
# PostgreSQL (primary database like Dify_MABOS)
psycopg2-binary==2.9.9
asyncpg==0.29.0
sqlalchemy==2.0.27
alembic==1.13.1

# Redis (caching and sessions like all reference codebases)
redis==5.0.1
redis-py-cluster==2.1.3
aioredis==2.0.1

# Elasticsearch (search and analytics)
elasticsearch==8.12.0
elasticsearch-dsl==8.12.0

# ===== Message Queue & Task Processing =====
# Celery (workflow execution like Kestra-KB patterns)
celery==5.3.6
flower==2.0.1
kombu==5.3.4

# Message Brokers
pika==1.3.2  # RabbitMQ
kafka-python==2.0.2

# ===== Workflow Orchestration =====
# YAML Processing (workflow definitions like Kestra-KB)
pyyaml==6.0.1
ruamel.yaml==0.18.6

# Workflow Validation
jsonschema==4.21.1
cerberus==1.3.5

# ===== Security & Authentication =====
# JWT & OAuth (enterprise auth like reference codebases)
pyjwt==2.8.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9

# OAuth Providers
authlib==1.3.0
python-social-auth[fastapi]==0.6.0
azure-identity==1.15.0
google-auth==2.28.0

# SAML Support
python3-saml==1.16.0

# ===== Data Validation & Serialization =====
# Pydantic (data validation like all reference codebases)
pydantic==2.6.0
pydantic-settings==2.1.0
email-validator==2.1.0

# ===== Web Scraping & Browser Automation (like Suna) =====
# Browser Automation
playwright==1.41.0
selenium==4.18.0
beautifulsoup4==4.12.3
scrapy==2.11.0

# ===== File Processing =====
# Document Processing
pypdf==4.0.1
python-docx==1.1.0
openpyxl==3.1.2
pandas==2.2.0
xlsxwriter==3.1.9

# Image Processing
pillow==10.2.0
opencv-python==4.9.0.80

# ===== Enterprise System Connectors =====
# SAP Integration
pyrfc==3.3.0
pyhdb==0.3.4

# Salesforce Integration
simple-salesforce==1.12.5
salesforce-bulk==2.2.0

# ServiceNow Integration
pysnow==0.7.17

# Microsoft 365 Integration
msgraph-core==0.2.2
azure-mgmt-resource==23.0.1
msal==1.26.0

# Oracle Integration
oracledb==1.4.2
cx-oracle==8.3.0

# ===== Monitoring & Observability =====
# Logging & Monitoring
structlog==24.1.0
loguru==0.7.2
prometheus-client==0.19.0
sentry-sdk[fastapi]==1.40.0

# Metrics & Tracing
opentelemetry-api==1.22.0
opentelemetry-sdk==1.22.0
opentelemetry-instrumentation-fastapi==0.43b0

# ===== Testing Framework =====
# Testing (comprehensive like reference codebases)
pytest==8.0.2
pytest-asyncio==0.23.5
pytest-cov==4.0.0
pytest-mock==3.12.0
pytest-xdist==3.5.0
httpx==0.27.0  # For testing HTTP clients
fakeredis==2.21.1

# Property-based Testing
hypothesis==6.99.0

# Load Testing
locust==2.23.1

# ===== Security Testing =====
# Security Scanning
bandit==1.7.7
safety==3.0.1

# ===== Development Tools =====
# Code Quality
black==24.2.0
isort==5.13.2
flake8==7.0.0
mypy==1.8.0
pre-commit==3.6.0

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==2.0.0
mkdocs==1.5.3
mkdocs-material==9.5.9

# ===== Configuration & Environment =====
# Environment Management
python-dotenv==1.0.1
dynaconf==3.2.4

# ===== Utility Libraries =====
# Date/Time Handling
arrow==1.3.0
dateutil==2.8.2

# HTTP Utilities
requests==2.31.0
urllib3==2.2.0

# Async Utilities
asyncio-mqtt==0.16.1
aiofiles==23.2.1

# Cryptography
cryptography==42.0.2
bcrypt==4.1.2

# Data Processing
numpy==1.26.4
scipy==1.12.0

# Configuration Management
click==8.1.7
typer==0.9.0

# ===== Deployment & DevOps =====
# Docker Support
docker==7.0.0

# Kubernetes Client
kubernetes==29.0.0

# Cloud SDKs
boto3==1.34.51  # AWS
azure-storage-blob==12.19.0  # Azure
google-cloud-storage==2.14.0  # GCP

# ===== Additional Enterprise Features =====
# Rate Limiting
slowapi==0.1.9
limits==3.8.0

# Background Jobs
apscheduler==3.10.4
rq==1.15.1

# Email
fastapi-mail==1.4.1
jinja2==3.1.3

# WebSocket Support
websockets==12.0
python-socketio==5.11.1

# Health Checks
health-check==1.3.3

# ===== Version Pinning =====
# Ensure compatibility
setuptools==69.1.0
wheel==0.42.0
pip==24.0
```

## Development Dependencies (requirements-dev.txt)

```python
# Development-specific dependencies
-r requirements.txt

# Enhanced Development Tools
ipython==8.21.0
jupyter==1.0.0
ipdb==0.13.13

# Performance Profiling
py-spy==0.3.14
memory-profiler==0.61.0
line-profiler==4.1.1

# Database Tools
pgcli==4.0.1
redis-cli==2.5.1

# API Documentation
redoc-cli==0.2.3
swagger-ui-bundle==0.0.9

# Load Testing
artillery==2.0.0
k6==0.49.0

# Security Testing Tools
semgrep==1.59.0
pip-audit==2.7.0
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry
│   ├── core/                      # Core BDI engine and framework
│   │   ├── __init__.py
│   │   ├── bdi/                   # BDI agent implementation
│   │   │   ├── agents.py          # Agent classes and lifecycle
│   │   │   ├── beliefs.py         # Belief system and knowledge
│   │   │   ├── desires.py         # Goal and desire management
│   │   │   ├── intentions.py      # Intention and planning
│   │   │   └── reasoning.py       # Reasoning engine
│   │   ├── ontology/              # Ontology management
│   │   │   ├── manager.py         # Owlready2 integration
│   │   │   ├── knowledge_graph.py # Neo4j integration
│   │   │   └── reasoning.py       # SPARQL and inference
│   │   ├── workflow/              # Workflow orchestration
│   │   │   ├── engine.py          # Workflow execution engine
│   │   │   ├── parser.py          # YAML workflow parser
│   │   │   ├── scheduler.py       # Task scheduling
│   │   │   └── monitoring.py      # Execution monitoring
│   │   └── config.py              # Core configuration
│   ├── api/                       # API routes and controllers
│   │   ├── __init__.py
│   │   ├── v1/                    # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── agents.py          # Agent management endpoints
│   │   │   ├── workflows.py       # Workflow endpoints
│   │   │   ├── auth.py            # Authentication endpoints
│   │   │   ├── integrations.py    # Enterprise integration endpoints
│   │   │   └── analytics.py       # Analytics and monitoring
│   │   └── dependencies.py        # FastAPI dependencies
│   ├── services/                  # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication and authorization
│   │   ├── llm_service.py         # LLM gateway and management
│   │   ├── integration_service.py # Enterprise system integrations
│   │   ├── sandbox_service.py     # Secure execution environment
│   │   └── analytics_service.py   # Analytics and monitoring
│   ├── models/                    # Database models and schemas
│   │   ├── __init__.py
│   │   ├── database.py            # Database configuration
│   │   ├── user.py                # User models
│   │   ├── agent.py               # Agent models
│   │   ├── workflow.py            # Workflow models
│   │   └── execution.py           # Execution models
│   ├── integrations/              # Enterprise system connectors
│   │   ├── __init__.py
│   │   ├── sap/                   # SAP integration
│   │   ├── salesforce/            # Salesforce integration
│   │   ├── servicenow/            # ServiceNow integration
│   │   ├── microsoft365/          # Microsoft 365 integration
│   │   └── oracle/                # Oracle integration
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   ├── logging.py             # Structured logging
│   │   ├── validators.py          # Data validation
│   │   ├── security.py            # Security utilities
│   │   └── helpers.py             # Common helpers
│   └── tests/                     # Test suites
│       ├── __init__.py
│       ├── unit/                  # Unit tests
│       ├── integration/           # Integration tests
│       ├── e2e/                   # End-to-end tests
│       └── fixtures/              # Test fixtures
├── migrations/                    # Database migrations
├── scripts/                       # Deployment and utility scripts
├── docs/                         # API documentation
├── docker/                       # Docker configurations
├── kubernetes/                   # Kubernetes manifests
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml               # Python project configuration
├── Dockerfile                   # Container definition
└── docker-compose.yml          # Local development setup
```

## Configuration Files

### Python Project Configuration (pyproject.toml)

```toml
[build-system]
requires = ["setuptools>=69.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mabos-backend"
version = "1.0.0"
description = "Multi-Agent Business Operating System Backend"
authors = [
    {name = "MABOS Development Team", email = "dev@mabos.ai"}
]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.urls]
Homepage = "https://github.com/mabos/backend"
Documentation = "https://docs.mabos.ai"
Repository = "https://github.com/mabos/backend.git"
"Bug Tracker" = "https://github.com/mabos/backend/issues"

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations/
  | __pycache__/
  | .git/
  | .venv/
  | build/
  | dist/
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["app"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
namespace_packages = true
exclude = [
    "migrations/",
    "build/",
    "dist/"
]

[[tool.mypy.overrides]]
module = [
    "owlready2.*",
    "neo4j.*",
    "playwright.*",
    "celery.*"
]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["app/tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=app",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=90",
    "--strict-markers",
    "--strict-config",
    "-v"
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "security: marks tests as security tests"
]

[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*"
]

[tool.bandit]
exclude_dirs = ["tests", "migrations"]
skips = ["B101", "B601"]

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
exclude = [
    ".git",
    "__pycache__",
    "migrations",
    ".venv",
    "build",
    "dist"
]
```

### Environment Configuration (.env.example)

```bash
# ===== Application Configuration =====
APP_NAME=MABOS
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-super-secret-key-here

# ===== Database Configuration =====
# PostgreSQL
DATABASE_URL=postgresql://mabos_user:mabos_password@localhost:5432/mabos_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30

# Neo4j (Knowledge Graph)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j_password

# Redis (Caching & Sessions)
REDIS_URL=redis://localhost:6379/0
REDIS_SESSION_DB=1
REDIS_CACHE_DB=2

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200
ELASTICSEARCH_INDEX_PREFIX=mabos

# ===== Authentication & Security =====
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# OAuth Providers
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
AZURE_TENANT_ID=your-azure-tenant-id

# ===== LLM Providers =====
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_AI_API_KEY=your-google-ai-api-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_API_KEY=your-azure-openai-key

# ===== Message Queue =====
# Celery
CELERY_BROKER_URL=redis://localhost:6379/3
CELERY_RESULT_BACKEND=redis://localhost:6379/4

# RabbitMQ (alternative)
RABBITMQ_URL=amqp://guest:guest@localhost:5672/

# ===== Enterprise Integrations =====
# SAP
SAP_HOST=your-sap-host
SAP_USERNAME=your-sap-username
SAP_PASSWORD=your-sap-password

# Salesforce
SALESFORCE_CLIENT_ID=your-salesforce-client-id
SALESFORCE_CLIENT_SECRET=your-salesforce-client-secret
SALESFORCE_USERNAME=your-salesforce-username
SALESFORCE_PASSWORD=your-salesforce-password

# ServiceNow
SERVICENOW_INSTANCE=your-servicenow-instance
SERVICENOW_USERNAME=your-servicenow-username
SERVICENOW_PASSWORD=your-servicenow-password

# ===== Monitoring & Observability =====
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
STRUCTURED_LOGGING=true

# ===== Cloud Storage =====
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-s3-bucket
AWS_REGION=us-east-1

# ===== Email Configuration =====
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-email-password
EMAIL_FROM=noreply@mabos.ai

# ===== Rate Limiting =====
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_BURST=200

# ===== Sandbox Configuration =====
SANDBOX_ENABLED=true
SANDBOX_TIMEOUT=300
SANDBOX_MEMORY_LIMIT=1024
```

## Key Technologies & Rationale

### Core Framework: FastAPI + Python 3.11+
- **Why**: Based on Dify_MABOS, MABOS-Standalone, and Suna showing excellent performance
- **Features**: High performance, automatic API documentation, async support, type hints

### BDI Implementation: Owlready2 + NetworkX + Neo4j
- **Why**: Dify_MABOS and MABOS-Standalone demonstrate sophisticated knowledge management
- **Benefits**: Ontology reasoning, knowledge graphs, semantic understanding

### Database Architecture: PostgreSQL + Neo4j + Redis + Elasticsearch
- **Why**: Multi-database approach from reference codebases for different data types
- **Benefits**: Relational data, graph relationships, caching, full-text search

### LLM Integration: LiteLLM + Multiple Providers
- **Why**: Comprehensive provider support across all reference codebases
- **Benefits**: Unified interface, failover, cost optimization

### Workflow Engine: Celery + YAML + Custom Engine
- **Why**: Kestra-KB workflow patterns with Python async capabilities
- **Benefits**: Distributed processing, declarative workflows, scalability

### Enterprise Integration: Direct API Clients
- **Why**: Direct integration patterns from enterprise-focused codebases
- **Benefits**: Native authentication, full feature access, optimal performance

This backend architecture provides:
- **Enterprise-grade** scalability and reliability
- **Comprehensive BDI** agent implementation
- **Multi-provider LLM** integration with intelligent routing
- **Secure execution** environment with sandbox isolation
- **Enterprise system** connectivity with major platforms
- **Real-time monitoring** and observability
- **Comprehensive testing** and quality assurance framework 