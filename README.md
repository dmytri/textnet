# TextNet: The Poem and Prompt Store

TextNet is a text-based shop where you can buy poems and prompts, accessible
via SSH. Built with Saleor Commerce and Charm bracelet's TUI Libraries
including Wish.

## Features

TextNet offers standard commerce features:
- Account creation and management
- Product browsing (poems and prompts)
- Shopping cart functionality
- Checkout process

In addition to these, TextNet includes multi-vendor capabilities:
- Products can be contributed by multiple authors
- Authors receive payouts when their works are sold

Currently, product management for authors is handled by the TextNet team via
Saleor Dashboard.

## Commerce Platform

TextNet uses Saleor Commerce as its core platform, deploying both Saleor Core
and Saleor Dashboard.

## Behaviour-Driven Automation (BDA)

This project uses Behaviour-Driven Automation for development and deployment.
Clone locally and use `tilt up` to start the development environment on your
Kubernetes cluster (e.g., minikube).

BDA extends Behaviour-Driven Development principles to automate:
- Alpine Linux VPS deployment for SSH-based storefront
- Kubernetes Jobs for BDA execution using pytest-bdd

Key components:
- Tilt for deployment automation
- Pytest-bdd for BDA execution
- Pyinfra for host configuration

## How It Works

The system uses BDA to:
- Provision infrastructure
- Configure environments (development, CI, production)
- Deploy and manage applications

## Getting Started

1. Install prerequisites:
   - Tilt
   - Minikube (or other Kubernetes cluster)

2. Clone the repository

3. Start the development environment: ```bash tilt up ```

## Contact

For questions, feedback, or contributions:
- [Dmytri Kleiner](mailto:dev@dmytri.to)
- [@dmytri.to](https://bluesky.social/@dmytri.to) on BlueSky

## Conventions

### Project Context
- Guide decisions using [Project Goals](GOALS.md) focus areas
- Current focuse is [VIBE](VIBE.md) focus areas
- Saleor installation reference: https://docs.saleor.io/setup/windows (adapting for Alpine Linux)

### Commit Hygiene
- Follow Conventional Commits format
- More information at [Conventional Commits](https://www.conventionalcommits.org/)
- Try to connect commits to current vibe and related bda/atdd scenarios

### Documentation & Text
- Use Canadian spelling for everything

### Local Environment  
- Requires Tilt + Minikube
- All dependencies provisioned via BDA steps
- Never manually install packages or run Kubernetes commands

### Saleor Commerce
- Saleor installation reference: https://docs.saleor.io/setup/windows (adapting for Alpine Linux)
- Saleor Platform Repository: [https://github.com/saleor/saleor-platform](https://github.com/saleor/saleor-platform)
- Saleor Platform Docker Compose: [https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml](https://raw.githubusercontent.com/saleor/saleor/blob/main/Dockerfile)

