from pytest_bdd import hooks

def pytest_bdd_before_scenario(request, feature, scenario):
    print(f"\nScenario: {scenario.name}")

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print(f"[✓] Step passed: {step.name}")

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"[✗] Step failed: {step.name}")
