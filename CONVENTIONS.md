# Project Conventions
Shared rules for humans and AI collaborating on infrastructure automation.

## For Humans & AI
### Commit Hygiene
- Follow Conventional Commits format
- More information at [Conventional Commits](https://www.conventionalcommits.org/)

### Documentation & Text
- Use Canadian spelling for all documentation (e.g., colour, centre, analyse)
- Prefer "-ise" over "-ize" in words like "organise"
- Use double consonants where appropriate (e.g., travelled, modelling)

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

### Third-Party Components
- Respect conventions specified by third-party components
- Use package managers and tools recommended in their documentation
- Do not impose project-specific conventions on third-party components

### Test Structure
- Feature files/step defs in `/tests`
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
- Each When step should focus on a single aspect of the desired state
- Run operations only at the end of the final When step in a sequence

### BDA Conventions
- Feature lines include 'BDA' identifier  
- Tags (@dev/@ci/@prod) control execution  
- When steps declare using pyinfra
- Then steps verify with pyinfra facts
- Use behaviour-focused, declarative language in all steps
- Focus on the desired state, not actions to achieve it
- Prefer atomic scenarios
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
1. NEVER edit files without explicit permission - always ask first
2. Suggest changes through SEARCH/REPLACE blocks only
3. Describe modifications in natural language first
4. Never execute commands or assume changes are applied
5. Trust human to handle actual git operations
6. When user says 'no', STOP immediately and do not suggest code
7. Displaying modified code requires explicit permission
8. Confirm understanding when suggestions are rejected
9. Make ONLY the minimal changes specifically requested
10. NEVER bundle unrelated changes without explicit approval

### Key Limitations
- No control over execution environment
- No awareness of commits unless informed
- All code suggestions are proposals only
