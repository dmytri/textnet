---
theme: dracula
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

- CXO at Saleor
- dk@saleor.io

| LinkedIn | [linkedin.com/in/dmytri](https://linkedin.com/in/dmytri) |
| Bluesky | @dmytri.to |
| Mastodon | dk@tldr.nettime.org |

---

# What is Behaviour-Driven Automation?

- Self-describing, self-verifying infrastructure automation
- Combines BDD (Behaviour-Driven Development) with IaC (Infrastructure as Code)
- Focuses on desired system behaviour, not implementation details
- Creates living documentation that evolves with your infrastructure

---

# BDA Core Principles

- **Declarative**: Focus on "what" not "how"
- **Idempotent**: Run steps multiple times with same result
- **Verifiable**: Each configuration step has a verification step
- **Readable**: Clear to both technical and non-technical stakeholders
- **Maintainable**: Evolves with your infrastructure needs

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

# Code Example

```javascript
function example() {
  console.log("Hello, world!");
}
```

---

# Thank You!

Questions?
