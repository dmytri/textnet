# Project Structure

This document outlines the purpose and organization of files and directories in this repository.

## Top-Level Directories

### `./` (Root Directory)
Contains configuration and setup files for Behaviour-Driven Automation (BDA) used in development, testing, and CI/CD. These are not part of the final deployed system.

### `target/`
Contains files for the target deployment environment (development/test). This is where the Saleor Commerce platform is deployed by BDA steps.

### `tests/` directory
Contains executable acceptance criteria (ATDD) and self-verifying automation steps (BDA) that validate infrastructure and application deployment.

## Key Files

### Root Directory Files
- `Dockerfile`: Builds the BDA test environment container for running pytest-bdd steps
- `manifest.yaml`: Kubernetes manifest for the BDA "Apply" job
- `Tiltfile`: Configures Tilt to automate deployment of both target host and BDA jobs
- `pyproject.toml`: Manages Python dependencies for BDA environment (development/testing only)

### Target Directory Files
- `Dockerfile`: Builds the Alpine Linux-based target host image for Saleor Commerce
- `manifest.yaml`: Kubernetes manifest for deploying the target host

### Tests Directory
- `deploy.feature`: Gherkin feature file defining infrastructure scenarios
- `test_deploy.py`: pytest-bdd step implementations for infrastructure verification

## BDA-Target System Relationship

The BDA setup:
1. Provisions a Kubernetes-based test environment using Tilt
2. Deploys the target system (defined in `target/`) to the environment
3. Executes automated tests from `tests/` to validate deployment correctness

Key Components:
- BDA tests verify infrastructure state using pyinfra facts
- Target Dockerfile creates the actual Saleor Commerce runtime environment
- Kubernetes manifests define deployment topology for both systems

