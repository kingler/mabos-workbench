#!/bin/bash

# MABOS Workbench - Dependency Installation Script
# This script installs all necessary dependencies for the MABOS project
# Following Task 24 testing requirements and project initialization guidelines

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_system_requirements() {
    log_info "Checking system requirements..."
    
    # Check Node.js version
    if command_exists node; then
        NODE_VERSION=$(node --version | cut -d'v' -f2)
        REQUIRED_NODE="18.17.0"
        if [ "$(printf '%s\n' "$REQUIRED_NODE" "$NODE_VERSION" | sort -V | head -n1)" = "$REQUIRED_NODE" ]; then
            log_success "Node.js version $NODE_VERSION is compatible"
        else
            log_error "Node.js version $NODE_VERSION is too old. Required: $REQUIRED_NODE or higher"
            exit 1
        fi
    else
        log_error "Node.js is not installed. Please install Node.js $REQUIRED_NODE or higher"
        exit 1
    fi
    
    # Check Python version
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        REQUIRED_PYTHON="3.11.0"
        if [ "$(printf '%s\n' "$REQUIRED_PYTHON" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_PYTHON" ]; then
            log_success "Python version $PYTHON_VERSION is compatible"
        else
            log_error "Python version $PYTHON_VERSION is too old. Required: $REQUIRED_PYTHON or higher"
            exit 1
        fi
    else
        log_error "Python 3 is not installed. Please install Python $REQUIRED_PYTHON or higher"
        exit 1
    fi
    
    # Check npm
    if ! command_exists npm; then
        log_error "npm is not installed. Please install npm"
        exit 1
    fi
    
    # Check pip
    if ! command_exists pip3; then
        log_error "pip3 is not installed. Please install pip3"
        exit 1
    fi
    
    # Check Docker (optional but recommended)
    if command_exists docker; then
        log_success "Docker is available"
    else
        log_warning "Docker is not installed. Some features may not work without Docker"
    fi
    
    # Check Docker Compose (optional but recommended)
    if command_exists docker-compose; then
        log_success "Docker Compose is available"
    else
        log_warning "Docker Compose is not installed. Some features may not work without Docker Compose"
    fi
}

# Install root dependencies
install_root_dependencies() {
    log_info "Installing root dependencies..."
    
    if [ -f "package.json" ]; then
        npm install
        log_success "Root dependencies installed"
    else
        log_warning "No package.json found in root directory"
    fi
}

# Install frontend dependencies
install_frontend_dependencies() {
    log_info "Installing frontend dependencies..."
    
    if [ -d "frontend" ]; then
        cd frontend
        
        if [ -f "package.json" ]; then
            # Install dependencies
            npm install
            
            # Install additional testing dependencies for Task 24
            log_info "Installing additional testing dependencies..."
            npm install --save-dev \
                @testing-library/jest-dom \
                @testing-library/react \
                @testing-library/user-event \
                @playwright/test \
                jest-environment-jsdom \
                jest-junit \
                jest-html-reporters \
                jest-sonar-reporter \
                identity-obj-proxy \
                @types/jest \
                eslint-plugin-testing-library \
                eslint-plugin-jest-dom
            
            log_success "Frontend dependencies installed"
        else
            log_error "No package.json found in frontend directory"
            exit 1
        fi
        
        cd ..
    else
        log_error "Frontend directory not found"
        exit 1
    fi
}

# Install backend dependencies
install_backend_dependencies() {
    log_info "Installing backend dependencies..."
    
    if [ -d "backend" ]; then
        cd backend
        
        # Create virtual environment if it doesn't exist
        if [ ! -d ".venv" ]; then
            log_info "Creating Python virtual environment..."
            python3 -m venv .venv
        fi
        
        # Activate virtual environment
        source .venv/bin/activate
        
        # Upgrade pip
        pip install --upgrade pip
        
        # Install requirements
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
            log_success "Backend dependencies installed"
        else
            log_error "No requirements.txt found in backend directory"
            exit 1
        fi
        
        # Install additional testing dependencies for Task 24
        log_info "Installing additional testing dependencies..."
        pip install \
            pytest-cov \
            pytest-html \
            pytest-xdist \
            pytest-mock \
            pytest-asyncio \
            pytest-timeout \
            bandit \
            safety \
            black \
            isort \
            flake8 \
            mypy \
            pre-commit
        
        # Deactivate virtual environment
        deactivate
        
        cd ..
    else
        log_error "Backend directory not found"
        exit 1
    fi
}

# Setup pre-commit hooks
setup_pre_commit_hooks() {
    log_info "Setting up pre-commit hooks..."
    
    if [ -d "backend" ]; then
        cd backend
        source .venv/bin/activate
        
        # Create pre-commit config if it doesn't exist
        if [ ! -f ".pre-commit-config.yaml" ]; then
            cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
  
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
EOF
        fi
        
        # Install pre-commit hooks
        pre-commit install
        
        deactivate
        cd ..
        
        log_success "Pre-commit hooks installed"
    fi
}

# Setup environment files
setup_environment_files() {
    log_info "Setting up environment files..."
    
    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# MABOS Environment Configuration

# Database Configuration
DATABASE_URL=postgresql://mabos_user:mabos_password@localhost:5432/mabos_db
REDIS_URL=redis://localhost:6379/0
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=mabos_password
ELASTICSEARCH_URL=http://localhost:9200

# API Keys (Replace with your actual keys)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Application Configuration
DEBUG=true
LOG_LEVEL=info
ENVIRONMENT=development

# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WEBSOCKET_URL=ws://localhost:8000/ws

# Enterprise Integration (Optional)
SAP_API_URL=
SAP_CLIENT_ID=
SAP_CLIENT_SECRET=
SALESFORCE_CLIENT_ID=
SALESFORCE_CLIENT_SECRET=
SERVICENOW_INSTANCE_URL=
SERVICENOW_CLIENT_ID=
SERVICENOW_CLIENT_SECRET=
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
ORACLE_CONNECTION_STRING=

# Testing Configuration
TESTING=false
TEST_DATABASE_URL=postgresql://test_user:test_password@localhost:5432/test_db
EOF
        log_success "Environment file created (.env)"
        log_warning "Please update the .env file with your actual API keys and configuration"
    else
        log_info "Environment file already exists"
    fi
}

# Create necessary directories
create_directories() {
    log_info "Creating necessary directories..."
    
    # Test directories
    mkdir -p tests/{integration,e2e,performance,security}
    mkdir -p frontend/__tests__/{unit,integration,e2e}
    mkdir -p backend/app/tests/{unit,integration,e2e,performance,security}
    
    # Documentation directories
    mkdir -p docs/{api,guides,specs}
    
    # Scripts directories
    mkdir -p scripts/{setup,build,deploy}
    
    # Infrastructure directories
    mkdir -p infrastructure/{docker,kubernetes,terraform}
    
    # Reports directories
    mkdir -p reports/{coverage,security,performance}
    
    log_success "Directories created"
}

# Install Playwright browsers
install_playwright_browsers() {
    log_info "Installing Playwright browsers..."
    
    if [ -d "frontend" ]; then
        cd frontend
        npx playwright install --with-deps
        cd ..
        log_success "Playwright browsers installed"
    fi
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."
    
    # Check frontend
    if [ -d "frontend" ]; then
        cd frontend
        if npm run type-check > /dev/null 2>&1; then
            log_success "Frontend TypeScript compilation successful"
        else
            log_warning "Frontend TypeScript compilation failed"
        fi
        cd ..
    fi
    
    # Check backend
    if [ -d "backend" ]; then
        cd backend
        source .venv/bin/activate
        
        if python -c "import app" > /dev/null 2>&1; then
            log_success "Backend Python imports successful"
        else
            log_warning "Backend Python imports failed"
        fi
        
        deactivate
        cd ..
    fi
    
    log_success "Installation verification completed"
}

# Main installation process
main() {
    log_info "Starting MABOS dependency installation..."
    
    # Check if we're in the right directory
    if [ ! -f "package.json" ] && [ ! -d "frontend" ] && [ ! -d "backend" ]; then
        log_error "This doesn't appear to be the MABOS project root directory"
        exit 1
    fi
    
    check_system_requirements
    create_directories
    install_root_dependencies
    install_frontend_dependencies
    install_backend_dependencies
    setup_pre_commit_hooks
    setup_environment_files
    install_playwright_browsers
    verify_installation
    
    log_success "MABOS dependency installation completed successfully!"
    echo
    log_info "Next steps:"
    echo "1. Update the .env file with your actual API keys"
    echo "2. Start the development services: npm run dev"
    echo "3. Run tests: npm run test"
    echo "4. Check the README.md for more information"
}

# Run main function
main "$@" 