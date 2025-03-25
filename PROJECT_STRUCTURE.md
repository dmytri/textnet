# Project Structure

This document outlines the purpose and organization of the files and directories in this repository.

## Top-Level Directories

*   `.`: Root directory
    *   Contains files related to the Behaviour-Driven Automation (BDA) setup. These are used for development, testing, and CI/CD, but are not part of the final deployed system.
*   `target`: Contains files related to the target system (e.g., the Saleor Commerce platform). This directory holds the configuration and deployment definitions for the actual application.
*   `tests`: Contains the BDD tests that verify the infrastructure and application deployment.

## Key Files and Directories

### Root Directory (`.`):

*   `.aider.conf.yml`: Configuration file for the aider AI assistant.
*   `.aider.model.settings.yml`: Model settings for the aider AI assistant.
*   `.dockerignore`: Specifies intentionally untracked files that Docker should ignore.
*   `.gitignore`: Specifies intentionally untracked files that Git should ignore.
*   `LICENSE.md`: License information for the project.
*   `conftest.py`: Pytest configuration file.
*   `manifest.yaml`: Kubernetes manifest for deploying the BDA test environment.
*   `pyrightconfig.json`: Configuration file for the Pyright type checker.
*   `pyproject.toml`: Defines project dependencies and scripts for the BDA environment (development, testing, CI/CD).  **NOTE:** This is for the BDA environment, *not* the target Saleor system.
*   `Tiltfile`: Configuration file for Tilt, used to automate the deployment of the BDA environment to a Kubernetes cluster.
*   `uv.lock`: Lockfile for uv package manager.
*   `Dockerfile`: Dockerfile for building the BDA test environment.

### Target Directory (`target`):

*   `Dockerfile`: Dockerfile for building the Saleor Commerce platform image.  **NOTE:** This is the Dockerfile for the *target* system.
*   `manifest.yaml`: Kubernetes manifest for deploying the Saleor Commerce platform.

### Tests Directory (`tests`):

*   `deploy.feature`: Feature file containing the Gherkin scenarios for testing the deployment of the Saleor Commerce platform.
*   `test_deploy.py`: Python file containing the pytest-bdd step definitions that implement the tests defined in `deploy.feature`.

## Relationship between BDA and Target System

The BDA setup in the root directory is used to:

1.  Provision a test environment (e.g., using Tilt and Kubernetes).
2.  Deploy the target system (defined in the `target` directory) to the test environment.
3.  Run automated tests (defined in the `tests` directory) to verify the correct deployment and configuration of the target system.

The `target` directory contains the necessary files to build and deploy the *actual* Saleor Commerce platform. The `tests` directory ensures that the platform is deployed and configured correctly.
