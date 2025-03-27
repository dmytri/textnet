# Project Vibe & Priorities

## Current Focus
Need to Implement Dashboard Steps
Tests failing: Step definition is not found: When "TNBP Saleor Dashboad service definition is present" (TNB).

## Current Issues
TNIB: Dashboard build tools

# AI Assistant
- When I ask something like *"what's the vibe?"* Tell me the current focus and issues
- When I say *update the vibe*, if I don't say with what, use that
- If there is a relevant step code, include it
- When asked to propose an update to this VIBE.md file, ignore the current "vibe" and focus solely on the instructions provided in the prompt.
- Never update any files other than this one (VIBE.md) when the topic is the vibe

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
*When you see that output, "Not implemented ..." in the test output, make
that the vibe, unless instructed otherwise*

Do not include examples when talking about the vibe
