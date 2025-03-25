# Project Conventions
- Project structure described here [Project Structure](PROJECT_STRUCTURE.md)
- Guide decisions using [Project Goals](GOALS.md)
- Current focus is kept in [VIBE](VIBE.md)
- Use Canadian spelling for everything

### Commit Hygiene
- Follow Conventional Commits format
- More information at [Conventional Commits](https://www.conventionalcommits.org/)
- Try to connect commits to current vibe and related bda/atdd scenarios

### Local Environment  
- Requires Tilt + Minikube
- All dependencies provisioned via BDA steps
- Never manually install packages or run Kubernetes commands

### Saleor Commerce
- Saleor installation reference: https://docs.saleor.io/setup/windows (adapting for Alpine Linux)
- Saleor Platform Repository: [https://github.com/saleor/saleor-platform](https://github.com/saleor/saleor-platform)
- Saleor Platform Docker Compose: [https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml](https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml)
- Saleor Dockerfile: [https://github.com/saleor/saleor/blob/main/Dockerfile](https://github.com/saleor/saleor/blob/main/Dockerfile)

### Pyinfra Patterns
```python
# Package installation
@when("Python runtime is available")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])
    run_ops(state)

# Version verification  
@then("Python version >= 3.12")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["python3"])[0]) >= parse("3.12")

```

- Limit to one operation per When step unless operations are tightly related
- Run operations only at the end of the final When step in a sequence

### Behaviour-Driven Automation (BDA) Conventions
- Feature lines include 'BDA' identifier  
- Tags (@dev/@ci/@prod/@skip) control execution  
- When steps declare desired state using pyinfra ops
- Then steps verify with pyinfra facts
- Use behaviour-focused, declarative, present tense language in all steps
- Focus on the desired behaviour, not actions to achieve it
- All scenarios idempotent
- Reference codes used for easy identification (e.g., TNFD)
  - First two letters: Feature identifier (TN = TextNet)
  - Third letter: Scenario identifier (A-Z)
  - Fourth character: Step identifier (alphanumeric)
  - Reference codes appear at the beginning of scenario/step descriptions

### Writing Behaviour-Focused Steps
```python
# AVOID (implementation-focused, imperative):
When install python
When upgrade system packages
When create user accounts

# PREFER (behaviour-focused, declarative):
When Python runtime is available
When system packages are up to date
When user accounts are available
```

### Saleor Commerce
- Saleor installation reference: https://docs.saleor.io/setup/windows (adapting for Alpine Linux)
- Saleor Platform Repository: [https://github.com/saleor/saleor-platform](https://github.com/saleor/saleor-platform)
- Saleor Platform Docker Compose: [https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml](https://raw.githubusercontent.com/saleor/saleor/blob/main/Dockerfile)
