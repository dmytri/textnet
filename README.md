# TextNet: The Poem and Prompt Store

### Saleor Commerce

TextNet uses Saleor Commerce as its e-commerce engine. This project deploys both Saleor Core and Saleor Dashboard on a host.

### Behaviour-Driven Automation (BDA)

This project uses Behaviour-Driven Automation for both development and deployment. Clone locally and use `tilt up` to run your development and test environment on your Kubernetes cluster (e.g., minikube for local development).

Behaviour-Driven Automation (BDA) extends Behaviour-Driven Development (BDD) principles to automate processes and workflows. In this project, BDA is used to:

🔹 Deploy an Alpine Linux VPS as a host for our terminal/SSH-based storefront
🔹 Use a Kubernetes Job to apply BDA to targets using pytest-bdd

Key components:
- Tilt for automating deployment and local development
- Pytest-bdd for BDA step execution
- Pyinfra for host configuration

### How It Works

The system uses BDA to:
- Provision infrastructure
- Configure environments (development, CI, production)
- Deploy and manage applications

### Getting Started

1. Install prerequisites:
   - Tilt
   - Minikube (or other Kubernetes cluster)

2. Clone the repository

3. Run `tilt up` to start the development environment

### Contact

For questions, feedback, or contributions, please contact [Dmytri Kleiner](mailto:dev@dmytri.to) or [@dmytri.to](https://bluesky.social/@dmytri.to) on BlueSky.

