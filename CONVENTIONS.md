# Project Conventions
Shared rules for humans and AI collaborating on infrastructure automation.

## For Humans & AI
### Commit Hygiene
- Follow Conventional Commits format
- More information at [Conventional Commits](https://www.conventionalcommits.org/)

### Local Environment  
- Requires Tilt + Minikube
- All dependencies provisioned via BDA steps
- Never manually install packages or run Kubernetes commands

### Python & Packaging
- Use `uv` for Python package management
- All dependencies in `pyproject.toml`

### Test Structure
- Feature files/step defs in `/tests`
- Use pytest-bdd with Gherkin syntax
- Follow ATDD principles (Given/When/Then)

### Pyinfra Patterns
```python
# Package installation
@when("python installed")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])
    run_ops(state)  # Final When runs all ops

# Version verification  
@then("python >= 3.12")
def _(host: Host):
    pkg = host.get_fact(ApkPackages).get("python3")
    assert parse(pkg) >= parse("3.12")
```

### Pyinfra Patterns
```python
# Package installation
@when("python installed")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])
    run_ops(state)  # Final When runs all ops

# Version verification  
@then("python >= 3.12")
def _(host: Host):
    pkg = host.get_fact(ApkPackages).get("python3")
    assert parse(pkg) >= parse("3.12")
```

### BDA Conventions
- Feature lines include 'BDA' identifier  
- Tags (@dev/@ci/@prod) control execution  
- When steps declare using pyinfra
- Then steps verify with pyinfra facts
- Prefer atomic scenarios
- All scenarios idempotent

## For AI Systems
### Change Protocol
1. Describe changes in natural language
2. Await explicit approval 
3. Provide SEARCH/REPLACE blocks
4. Never execute commands directly
5. Only modify test steps when explicitly requested - scenario additions in feature files do NOT require immediate step implementations

### Test Execution
- Only through Tilt/BDA pipeline
- Never suggest manual pytest runs
