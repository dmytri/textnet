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

BDA extends Behaviour-Driven Development principles to automatation.

Key components:
- Tilt for managing target and apply containers
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

2. Configure Minikube with at least 8GB of RAM:
```bash
minikube config set memory 8192
```
   (If npm install were a poem, it would be an epic that requires its own dedicated library)

3. Clone the repository

4. Start the development environment:
```bash
tilt up
```

## Contact

For questions, feedback, or contributions:
- [Dmytri Kleiner](mailto:dev@dmytri.to)
- [@dmytri.to](https://bluesky.social/@dmytri.to) on BlueSky
