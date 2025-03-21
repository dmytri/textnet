import pytest
from pytest_bdd.parser import Step

# Hooks to show clean pass/fail markers for each step
@pytest.hookimpl(trylast=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Mark steps that pass with a checkmark."""
    print(f"✓ {step.keyword} {step.name}")

@pytest.hookimpl(trylast=True)
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Mark steps that fail with an X."""
    print(f"✗ {step.keyword} {step.name}")
    
    # If this is a "no hosts remaining" error, try to show the original cause
    if "no hosts remaining" in str(exception):
        print("\nNOTE: 'No hosts remaining' is usually a secondary effect.")
        print("Original error may be in the traceback below.")
