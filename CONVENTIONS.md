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
- Use behavior-focused, declarative language in all steps
- Focus on the desired state, not actions to achieve it
- Prefer atomic scenarios
- All scenarios idempotent

### Writing Behavior-Focused Steps
```python
# AVOID (implementation-focused, imperative):
When install python
When upgrade system packages
When create user accounts

# PREFER (behavior-focused, declarative):
When Python runtime is available
When system packages are up to date
When user accounts are available
```

## For AI Systems
### AI Assistant Role
1. NEVER edit files without explicit permission - always ask first
2. Suggest changes through SEARCH/REPLACE blocks only
3. Describe modifications in natural language first
4. Never execute commands or assume changes are applied
5. Trust human to handle actual git operations

### Key Limitations
- No control over execution environment
- No awareness of commits unless informed
- All code suggestions are proposals only
