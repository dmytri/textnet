# Project Structure

- [`Dockerfile`](./Dockerfile): Apply container for running pytest-bdd steps
- [`manifest.yaml`](./manifest.yaml): Kubernetes manifest for the BDA "Apply" job
- [`Tiltfile`](./Tiltfile): Configures Tilt to automate deployment of both target host and BDA jobs
- [`pyproject.toml`](./pyproject.toml): Manages Python dependencies for BDA environment

- `target/`: Dockerfile and Manifest used by Tilt to create target host container wthat is configured by BDA
- [`target/Dockerfile`](./target/Dockerfile): Builds the Alpine Linux-based target host image
- [`target/manifest.yaml`](./target/manifest.yaml): Kubernetes manifest for deploying the target host

- `tests/`: Pytest test files for self describing, self-verifying automation (BDA)
- [`tests/deploy.feature`](./tests/deploy.feature): Gherkin feature file defining deploy scenarios
- [`tests/test_deploy.py`](./tests/test_deploy.py): pytest-bdd step implementations for scenario steps

## BDA-Target System Relationship

- BDA When steps configure the target host using pyinfra ops
- BDA Then steps verify state using pyinfra facts

The BDA setup:
1. Provisions a Kubernetes-based environment using Tilt
2. Deploys the target system (defined in `target/`) to the environment
3. Executes automated tests from `tests/` to validate deployment correctness

