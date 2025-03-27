# Curremt Vibe: Project Vibe & Priorities

## Current Focus
Need to Implement Dashboard Steps
Tests failing: Step definition is not found: When "TNBP Saleor Dashboad service definition is present" (TNB).

## Current Issues
TNIB: Dashboard build tools

# AI Assistant
- When I ask something like *"what's the vibe?"* Tell me the current focus and issues
- When I say "update the vibe" without providing new content:
  - I am indicating that you should analyze recent test output
  - Focus on any failed tests and errors in the test output
  - Focus on any "Not implemented:" steps in the test output
  - Update the vibe to the steps that are failing or not implemented
  - Include the relevant step code in the vibe update.

**Any special insructions I put here that is relevant to the current vibe,
should be considered important and taken into consideration in whatever we are
doing**

## Examples

## Step stub

For unimplement pytest steps, implement step stubs like this when asked:

```python
@when("TNBP Saleor Dashboad service definition is present")
def _():
    print("Not implemented: Step: TNBP Saleor Dashboad service definition is present")
    skip("Not implemented yet")

``````

Do not include examples when talking about the vibe

