---
theme: the-unnamed
background: black
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## BDA & Commerce as Code
  Presentation slides
---

# Behaviour-Driven Automation
# Commerce as Code

---

# Dmytri Kleiner

## CXO at Saleor

| Platform | Contact |
|----------|---------|
| LinkedIn | [linkedin.com/in/dmytri](https://linkedin.com/in/dmytri) |
| Bluesky | @dmytri.to |
| Mastodon | dk@tldr.nettime.org |

---

# My Journey & Lessons Learned

| Company | Role | Key Lessons |
|---------|------|-------------|
| Saleor | CXO | Commerce as code, API-driven commerce |
| Contentful | Senior Solution Architect | Headless architecture, content modeling |
| Red Hat | Senior Architect | Open source collaboration, Containers, DevOps |
| ThoughtWorks | Lead Analyst | Agile delivery, XP practices, TDD/BDD, CI/CD |
| SoundCloud | Architecture Developer | Building scalable platforms, Immutable Hosts, BFF |

---
# What is Commerce as Code

- [Commerce as Code](https://app.excalidraw.com/p/6eOL2YRYSdU/61VF5112gAa:w

---

# What is Behaviour-Driven Automation?

- Self-describing, self-verifying infrastructure automation
- Combines BDD (Behaviour-Driven Development) with IaC (Infrastructure as Code)
- Focuses on desired system behaviour, not implementation details
- Creates living documentation that evolves with your infrastructure

---

# Local Development with Tilt & Minikube

- **Minikube**: Lightweight Kubernetes for local development
  - Runs a single-node Kubernetes cluster in a VM
  - Perfect for testing Kubernetes applications locally

- **Tilt**: Modern dev environment orchestrator
  - Watches your files for changes and rebuilds/deploys automatically
  - Provides real-time feedback on your services
  - Simplifies the development workflow

- **Our Setup**:
  - BDA tests run in Kubernetes pods
  - Target system deployed as separate container
  - Changes to code trigger automatic redeployment
  - Live logs and debugging information in Tilt UI

---

# BDA in Practice: Gherkin Syntax

```gherkin
Feature: Saleor Commerce Platform | BDA

  Scenario: Provide Saleor commerce capabilities
    When build tools are available
     And Saleor database is setup
     And Saleor source code is available
     And Saleor Python dependencies are installed
     And Saleor service is enabled
    Then Saleor is operational
```

---

# BDA Implementation with PyInfra

```python
@when("Python runtime is available")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])
    run_ops(state)

@then("Python version >= 3.12")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["python3"])[0]) >= parse("3.12")
```
---

# Benefits of BDA

- **Documentation**: Features and scenarios serve as living documentation
- **Collaboration**: Common language between technical and business teams
- **Reliability**: Consistent, repeatable infrastructure deployments
- **Testing**: Built-in verification of infrastructure state
- **Maintainability**: Clear separation of concerns and modular design

---

# BDA vs Traditional Approaches

| Traditional Approach | BDA Approach |
|----------------------|--------------|
| Imperative scripts   | Declarative specifications |
| Manual verification  | Automated verification |
| Technical focus      | Behaviour focus |
| Separate docs        | Self-documenting code |
| Implementation-specific | Implementation-agnostic |

---

# Thank You!

Questions?
