# Project Structure

This document outlines the purpose and organization of files and directories in this repository.

## Top-Level Directories

### `.` (Root Directory)
+Contains configuration and setup files for Behaviour-Driven Automation (BDA) used in development, testing, and CI/CD. These are not part of the final deployed system.

-Contains files related to the Behaviour-Driven Automation (BDA) setup.
-These are used for development, testing, and CI/CD, but are not part of the
-final deployed system.
-
-### `target` directory
-
-Contains files related to the deploy target host for dev and tests enviroments.
-This is where the system will be depoloyed to by the BDA steps in dev and test
-enviroments.
+### `target`
+Contains files for the target deployment environment (development/test). This is where the Saleor Commerce platform is deployed by BDA steps.

### `tests` directory
-
-Contains the BDA and ATDD steps that provide the self-describing, and
-self-verifying automation steps (BDA) as well as the executable acceptance
-criteria (ATDD)
+Contains executable acceptance criteria (ATDD) and self-verifying automation steps (BDA) that validate infrastructure and application deployment.

## Key Files

-### `.`: Root directory
+### Root Directory Files
+- `Dockerfile`: Builds the BDA test environment container for running pytest-bdd steps
+- `manifest.yaml`: Kubernetes manifest for the BDA "Apply" job
+- `Tiltfile`: Configures Tilt to automate deployment of both target host and BDA jobs
+- `pyproject.toml`: Manages Python dependencies for BDA environment (development/testing only)
+- `uv.lock`: Lockfile for UV package manager

-* `Dockerfile`: Dockerfile for running BDA/ATDD Steps in Apply job
-* `manifest.yaml`: Kubernetes manifest for the Apply, uses the above Dockerfile
-* `Tiltfile`: Configuration file for Tilt, used to automate the deployment the Target host and run the Apply job
-
-### Target Directory (`target`):
-
-* `Dockerfile`: Dockerfile for target host to be used in Dev and Test enviroments
-* `manifest.yaml`: Kubernetes manifest for deploying the target host.
+### Target Directory Files
+- `Dockerfile`: Builds the Alpine Linux-based target host image for Saleor Commerce
+- `manifest.yaml`: Kubernetes manifest for deploying the target host

-## Relationship between BDA and Target System
+### Tests Directory
+- `deploy.feature`: Gherkin feature file defining infrastructure scenarios
+- `test_deploy.py`: pytest-bdd step implementations for infrastructure verification

-The BDA setup in the root directory is used to:
+## BDA-Target System Relationship

-1.  Provision a test host as described in the `target` directory, using Tilt
-2.  Deploy the system to the target host.
-3.  Run automated tests (defined in the `tests` directory) to verify the correct deployment and configuration of the target system.
+The BDA setup:
+1. Provisions a Kubernetes-based test environment using Tilt
+2. Deploys the target system (defined in `target/`) to the environment
+3. Executes automated tests from `tests/` to validate deployment correctness

-
+Key Components:
+- BDA tests verify infrastructure state using pyinfra facts
+- Target Dockerfile creates the actual Saleor Commerce runtime environment
+- Kubernetes manifests define deployment topology for both systems
+

Contains files related to the Behaviour-Driven Automation (BDA) setup.
These are used for development, testing, and CI/CD, but are not part of the
final deployed system.

### `target` directory

Contains files related to the deploy target host for dev and tests enviroments.
This is where the system will be depoloyed to by the BDA steps in dev and test
enviroments.

### `tests` directory

Contains the BDA and ATDD steps that provide the self-describing, and
self-verifying automation steps (BDA) as well as the executable acceptance
criteria (ATDD)

## Key Files

### `.`: Root directory

* `Dockerfile`: Dockerfile for running BDA/ATDD Steps in Apply job
* `manifest.yaml`: Kubernetes manifest for the Apply, uses the above Dockerfile
* `Tiltfile`: Configuration file for Tilt, used to automate the deployment the Target host and run the Apply job

### Target Directory (`target`):

* `Dockerfile`: Dockerfile for target host to be used in Dev and Test enviroments
* `manifest.yaml`: Kubernetes manifest for deploying the target host.

## Relationship between BDA and Target System

The BDA setup in the root directory is used to:

1.  Provision a test host as described in the `target` directory, using Tilt
2.  Deploy the system to the target host.
3.  Run automated tests (defined in the `tests` directory) to verify the correct deployment and configuration of the target system.

