# Curremt Vibe: Project Vibe & Priorities

## Current Focus
Need to implement the "TNB Provide Saleor Dashboard" scenario steps and resolve the "TNIB build tools are available" issue.

## Current Issues
- `@when("TNBP Saleor Dashboad service definition is present")` is not implemented.
- `@when("TNBE Saleor Dashboard service is enabled")` is not implemented.
- `@then("TNBX Host has converged")` is not implemented.
- `@then("TNBV Saleor Dashboad is operational")` is not implemented.
- TNIB: Dashboard build tools are not properly configured.

# AI Assistant
- When I ask something like *"what's the vibe?"* Tell me the current focus and issues
  - Just answer and don't do anything or offer to do anything
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

