# Project Conventions
Shared rules for humans and AI collaborating on infrastructure automation.
See also: [Project Structure](PROJECT_STRUCTURE.md)

## For Humans & AI
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

### Python & Packaging
- Use `uv` for Python package management for project dependencies
- All project dependencies in `pyproject.toml`
- For third-party components with their own package managers (e.g. Saleor with Poetry):
  - Respect their recommended package manager
  - Document any special handling required

### Saleor Commerce
- Saleor installation reference: https://docs.saleor.io/setup/windows (adapting for Alpine Linux)
- Saleor Platform Repository: [https://github.com/saleor/saleor-platform](https://github.com/saleor/saleor-platform)
- Saleor Platform Docker Compose: [https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml](https://raw.githubusercontent.com/saleor/saleor-platform/refs/heads/main/docker-compose.yml)
- Saleor Dockerfile: [https://github.com/saleor/saleor/blob/main/Dockerfile](https://github.com/saleor/saleor/blob/main/Dockerfile)

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
- Reference codes used for easy identification (e.g., SCF6)
  - First two letters: Feature identifier (SC = Saleor Commerce)
  - Third letter: Scenario identifier (A-Z)
  - Fourth character: Step number (alphanumeric)
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
- ALWAYS cross-reference requests against [VIBE.md](VIBE.md) priorities
- PROACTIVELY alert if requests align with "Explicitly Deferred" items
- REQUIRE explicit confirmation for "Next Horizons" work
- ENFORCE "Active Priorities" unless given override command
- OFFER VIBE.md updates before expanding scope
- NEVER assume priority changes without documentation updates
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

### Enforcement Protocol
1. For every request:
   - Check against VIBE.md's **Active Priorities** (🔥)
   - Verify against **Explicitly Deferred** (❄️) 
2. If mismatched:
   - State conflict with direct VIBE.md quotes
   - Present options:
     a) Update VIBE.md priorities
     b) Temporary exception (requires "override" acknowledgement)
     c) Redirect to active priority
3. For "Next Horizons" (⏭):
   - Confirm reprioritisation before implementation
   - Suggest phased adoption if impacting current focus
