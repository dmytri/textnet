
def pytest_bdd_before_scenario(request, feature, scenario):
    print(f"\n\033[34mScenario: {scenario.name}\033[0m")

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    print(f"\033[32m ✅ Step passed: {step.name}\033[0m")

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"\033[31m 💥 Step failed: {step.name}\033[0m")
