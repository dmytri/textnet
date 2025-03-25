# Project Vibe & Priorities

## Current Focus 🧠
**Saleor Version Verification & Service Enablement TNS**
*Ensuring Saleor is properly installed and operational, with accurate version
detection and reliable service enablement. Resolving the "git not found" issue
during service enablement is a priority.*

## Current Issues 🐛
**Failure in TNS Scenario: Saleor Version Verification**
*The TNS scenario, specifically the "TNSV saleor version >= 3.20" step, is
failing due to `packaging.version.InvalidVersion: Invalid version: ''`. This
indicates that the `poetry version` command is not returning a valid version
string.*

**Failure in TNS Scenario: Saleor Service Enablement**
*The TNS scenario, specifically the "TNSE Saleor service is enabled" step, is failing because the `git` command is not found. This prevents the service from being properly enabled.*
