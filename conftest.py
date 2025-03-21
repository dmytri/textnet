import pytest
from _pytest.runner import CallInfo
from pytest_bdd.steps import Step, get_step_fixture_name
from pyinfra.exceptions import PyinfraError

# Hook to improve error reporting for BDD steps
@pytest.hookimpl(trylast=True)
def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Log each step as it completes successfully."""
    step_name = f"{step.keyword} {step.name}"
    print(f"✓ {step_name}")

@pytest.hookimpl(trylast=True)
def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Improve error reporting for failed steps."""
    step_name = f"{step.keyword} {step.name}"
    print(f"✗ {step_name}")
    
    # Prevent "no hosts remaining" from obscuring the real error
    if isinstance(exception, PyinfraError) and "no hosts remaining" in str(exception):
        print("\nActual error that caused test failure:")
        if hasattr(exception, "__cause__") and exception.__cause__ is not None:
            print(f"  {type(exception.__cause__).__name__}: {exception.__cause__}")
        elif hasattr(exception, "__context__") and exception.__context__ is not None:
            print(f"  {type(exception.__context__).__name__}: {exception.__context__}")

# Filter out "no hosts remaining" from terminal output
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Clean up terminal report to remove misleading 'no hosts remaining' messages."""
    if exitstatus != 0:  # Only process on test failures
        # Access the reports
        for report_type in ('failed', 'errors'):
            for report in getattr(terminalreporter, report_type, []):
                if hasattr(report, 'longrepr') and report.longrepr:
                    # If the error is about "no hosts remaining", add context
                    if "no hosts remaining" in str(report.longrepr):
                        report.sections.append(
                            ("Note", "The 'no hosts remaining' error is a secondary effect. See the actual failure above.")
                        )
