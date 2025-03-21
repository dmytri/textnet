# Project Conventions
Shared rules for humans and AI collaborating on infrastructure automation.

## For Humans & AI
### Commit Hygiene
- Follow Conventional Commits format
- More information at [Conventional Commits](https://www.conventionalcommits.org/)

### Documentation & Text
- Use Canadian spelling for all documentation (e.g., colour, centre, analyse)

### Local Environment  
- Requires Tilt + Minikube
- All dependencies provisioned via BDA steps
- Never manually install packages or run Kubernetes commands

### Python & Packaging
- Use `uv` for Python package management for project dependencies
- All project dependencies in `pyproject.toml`
- For third-party components with their own package managers (e.g. Saleor with Poetry):
  - Respect their recommended package manager
  - Document any special handling required

### Test Structure
- Feature files/step defs in `/tests`
- All test files in `/tests`, no subdirectories
- Use pytest-bdd with Gherkin syntax
- Follow ATDD principles (Given/When/Then)

### Pyinfra Patterns
```python
# Package installation
@when("Python runtime is available")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])
    run_ops(state)  # Final When runs all ops

# Version verification  
@then("python version >= 3.12")
def _(host: Host):
    pkg = host.get_fact(ApkPackages).get("python3")
    assert parse(pkg) >= parse("3.12")
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

### Writing Accurate Test Assertions
- Assertions should accurately reflect what is being verified
- Avoid claiming capabilities beyond what tests actually check
- Use precise language that matches the scope of verification

```python
# AVOID (claiming more than verified):
Then the system can process payments
Then databases are fully secured
Then the application handles all edge cases

# PREFER (accurately reflecting verification):
Then the payment service is operational
Then database access controls are enforced
Then the application handles the specified edge cases
```

## For AI Systems
### AI Assistant Role
- ALWAYS describe modifications in natural language first
- ALWAYS make ONLY the minimal changes specifically requested
- ALWAYS stop immediately when user says 'no'
- NEVER edit files without explicit permission - ask first
- NEVER bundle unrelated changes without explicit approval
- NEVER execute commands or assume changes are applied
- ALWAYS wait for explicit instructions about what changes are wanted
- NEVER make assumptions about what the user wants to change
- ONLY provide analysis or information unless explicitly asked to make changes
- ALWAYS ask for permission before suggesting modifications
- ALWAYS be explicit about what you're being asked to do before taking action
- NEVER switch contexts or start working on new topics without being explicitly asked
- ALWAYS stay focused on the current topic until given a new task
