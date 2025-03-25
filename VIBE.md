# Project Vibe & Priorities

## Current Focus 🧠
**Saleor Version Verification TNSV**
*Ensuring Saleor is properly installed and operational, with accurate version
detection.*

## Current Issues 🐛
**Failure in TNS Scenario: Saleor Version Verification**
*The TNS scenario, specifically the "TNSV saleor version >= 3.20" step, is
failing due to `packaging.version.InvalidVersion: Invalid version: ''`. This
indicates that the `poetry version` command is not returning a valid version
string.*
