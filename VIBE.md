# Project Vibe & Priorities

## Current Focus 🧠
**Saleor Version Verification TNSV**
*Ensuring Saleor is properly installed and operational, with accurate version
detection.*

**Saleor Dashboard Integration**
*Adding scenarios to ensure the Saleor dashboard dependencies are installed and the dashboard is accessible.*

## Current Issues 🐛
**Failure in TNS Scenario: Saleor Version Verification**
*The TNS scenario, specifically the "TNSV saleor version >= 3.20" step, is
failing due to `packaging.version.InvalidVersion: Invalid version: ''`. This
indicates that the `poetry version` command is not returning a valid version
string.*

**Need to Implement Dashboard Steps**
*The "TNDB Ensure Saleor Dashboard Dependencies are Installed" and "TNDC Provide Saleor Dashboard" scenarios have been added to `deploy.feature`, but the corresponding step definitions are not yet implemented in `tests/test_deploy.py`.*
