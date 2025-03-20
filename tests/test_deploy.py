from typing import Literal, TypedDict

from pyinfra.api.config import Config
from pyinfra.api.connect import connect_all
from pyinfra.api.host import Host
from pyinfra.api.inventory import Inventory
from pyinfra.api.operation import add_op
from pyinfra.api.operations import run_ops
from pyinfra.api.state import State
from pyinfra.facts.apk import ApkPackages
from pyinfra.facts.server import LinuxDistribution, LinuxDistributionDict
from pyinfra.facts.server import Command
from pyinfra.facts.files import Directory
from pyinfra.operations import apk, files, server, init
from packaging.version import parse
from pytest import fixture, skip
from pytest_bdd import given, scenario, scenarios, then, when

## GLOBALS AND FIXTURES ~
#

Targets = Literal["ci", "dev", "prod"] 
TARGET: Targets | None = None

@fixture
def host(state: State) -> Host:
    assert state.inventory.hosts
    host: Host = list(state.inventory.hosts.values())[0]

    assert host is not None
    return host

@fixture
def state() -> State:
    global TARGET
    assert TARGET is not None
    match TARGET:
        case "dev":
            inventory: Inventory = Inventory((
                ["localhost"],
                {
                    "ssh_user": "root",
                    "ssh_port": 2222,
                    "ssh_password": "xxxxxxxx",
                    "ssh_strict_host_key_checking": "off",
                    "ssh_known_hosts_file": "/dev/null",
                }
            ))
        case "ci":
            inventory: Inventory = Inventory((
                ["ssh-service"],
                {
                    "ssh_user": "root",
                    "ssh_port": 2222,
                    "ssh_password": "xxxxxxxx",
                    "ssh_strict_host_key_checking": "off",
                    "ssh_known_hosts_file": "/dev/null",
                }
            ))
        case "prod":
            inventory: Inventory = Inventory((
                ["teknik.net"],
                {
                    "ssh_user": "dk",
                    "ssh_port": 22,
                    "ssh_password": "xxxxxxxx",
                    "ssh_strict_host_key_checking": "off",
                    "ssh_known_hosts_file": "/dev/null",
                }
            ))

    state = State(inventory, Config())

    state.print_input = True
    state.print_output = True
    state.print_fact_info = True
    state.print_noop_info = True

    connect_all(state)

    return state

SOFT_SERVE_VERSION: str | None = None

class SoftServe(TypedDict):
    version: str
    pkg: str

DEPLOYED: bool = False

@fixture
def deployed() -> bool:
    assert (isinstance(DEPLOYED, bool))
    return DEPLOYED

## SCENARIOS ~
#

scenarios("deploy.feature")

## PREFLIGHT SCENARIOS
#

scenario("deploy.feature", "Target a development environment for testing")

@when("set target environment to dev")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "dev"

@then("the system is configured for development testing")
def _():
    global TARGET
    assert TARGET == "dev"

scenario("deploy.feature", "Target a CI environment for verification")

@when("set target environment to ci")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "ci"

@then("the system is configured for continuous integration")
def _():
    global TARGET
    assert TARGET == "ci"

scenario("deploy.feature", "Target a production environment for customers")

@when("set target environment to prod")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "prod"

@then("the system is configured for production use")
def _():
    global TARGET
    assert TARGET == "prod"

## DEPLOY SCENARIOS ~
#

scenario("deploy.feature", "Provide a stable Alpine Linux platform")

@when("system packages up to date")
def _(state: State, deployed: bool):
    if deployed:
        skip()

    # Ensuring system packages are current
    add_op(state,
       apk.update
    )
    add_op(state,
       apk.upgrade
    )

    run_ops(state)

@then("OS Alpine Linux 3.21")
def _(host: Host):
    distro: LinuxDistributionDict = host.get_fact(LinuxDistribution)
    assert distro["release_meta"]["PRETTY_NAME"] == "Alpine Linux v3.21"

scenario("deploy.feature", "Enable required runtime environments for Saleor")

@when("Python runtime is available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    add_op(state, apk.packages, packages=["python3"])

@when("NodeJS runtime is available") 
def _(state: State, deployed: bool):
    if deployed:
        skip()
    add_op(state, apk.packages, packages=["nodejs"])

@when("SQLite database is available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    add_op(state, apk.packages, packages=["sqlite"])

@when("Poetry is available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Install Poetry using the official installer as per their documentation
    add_op(
        state,
        server.shell,
        commands=[
            "python3 -m pip install --user --break-system-packages poetry"
        ],
    )
    run_ops(state)


@then("python version >= 3.12")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert "python3" in packages
    pkg_version = packages["python3"]
    if isinstance(pkg_version, set):
        pkg_version = list(pkg_version)[0]
    assert parse(pkg_version) >= parse("3.12")

@then("nodejs version >= 18")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert "nodejs" in packages
    pkg_version = packages["nodejs"]
    if isinstance(pkg_version, set):
        pkg_version = list(pkg_version)[0]
    assert parse(pkg_version) >= parse("18")

@then("sqlite version >= 3.48.0")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert "sqlite" in packages
    pkg_version = packages["sqlite"]
    if isinstance(pkg_version, set):
        pkg_version = list(pkg_version)[0]
    assert parse(pkg_version) >= parse("3.48.0")

@then("the platform can run Saleor components")
def _(host: Host):
    # This higher-level assertion verifies that all required runtime
    # capabilities for Saleor are present
    packages = host.get_fact(ApkPackages)
    assert "python3" in packages
    assert "nodejs" in packages
    assert "sqlite" in packages
    
@then("poetry version >= 1.8")
def _(host: Host):
    cmd_result = host.get_fact(Command, command="poetry --version | awk '{print $3}'")
    assert parse(cmd_result['stdout'].strip()) >= parse("1.8")

## SALEOR INSTALLATION SCENARIO
#

scenario("deploy.feature", "Provide Saleor commerce capabilities")

@given("Saleor dependencies are installed")
def _(host: Host):
    # Verify all required dependencies exist
    packages = host.get_fact(ApkPackages)
    assert "python3" in packages
    assert "nodejs" in packages
    assert "sqlite" in packages

@when("build dependencies are available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Install git and required dependencies for building Saleor
    add_op(state, apk.packages, packages=["git", "python3-dev", "build-base", "py3-pip"])

@when("Poetry package manager is installed")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Install Poetry as recommended by Saleor documentation
    add_op(
        state,
        server.shell,
        commands=[
            "pip3 install poetry"
        ],
    )

@when("Saleor source code is available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Ensure Saleor source code is present
    add_op(
        state,
        server.shell,
        commands=[
            "test -d /opt/saleor || git clone https://github.com/saleor/saleor.git /opt/saleor"
        ],
    )

@when("Saleor Python components are installed")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Install Saleor Python dependencies using Poetry as per documentation
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && poetry install"
        ],
    )

@when("Saleor service definition is present")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Create OpenRC init script for Saleor
    add_op(
        state,
        files.put,
        src_string="""#!/sbin/openrc-run

name="Saleor Commerce Platform"
description="Saleor API and commerce services"
supervisor=supervise-daemon
command="/usr/bin/poetry"
command_args="run uvicorn saleor.asgi:application --host 0.0.0.0 --port 8000"
directory="/opt/saleor"
pidfile="/run/saleor.pid"
output_log="/var/log/saleor.log"
error_log="/var/log/saleor.err"

depend() {
    need net
    after firewall
}
""",
        dest="/etc/init.d/saleor",
        mode="0755",
    )

@when("Saleor service is enabled")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    # Enable and start the Saleor service using OpenRC
    add_op(state, init.rc, service="saleor", running=True, enabled=True)
    run_ops(state)

@then("saleor version >= 3.20")
def _(host: Host):
    # Check saleor version using poetry
    cmd_result = host.get_fact(Command, command="cd /opt/saleor && poetry version | awk '{print $2}' || echo '0.0.0'")
    version = cmd_result['stdout'].strip()
    assert parse(version) >= parse("3.20")

@then("saleor service is running")
def _(host: Host):
    # Check if service is running using OpenRC
    cmd_result = host.get_fact(Command, command="rc-service saleor status | grep -q 'started' && echo 'running'")
    assert cmd_result['stdout'].strip() == "running"
    
    # Check if saleor directory exists
    saleor_dir = host.get_fact(Directory, name="/opt/saleor")
    assert saleor_dir is not None

@then("Saleor commerce platform is operational")
def _(host: Host):
    # Test the GraphQL endpoint to see if it's responding
    cmd_result = host.get_fact(Command, command="curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/graphql/")
    status_code = cmd_result['stdout'].strip()
    assert status_code in ["200", "400"]  # 400 can occur when sending an empty request, which is still valid
