from io import StringIO
from textwrap import dedent
from typing import Literal, Optional

from pyinfra.api.config import Config
from pyinfra.api.connect import connect_all
from pyinfra.api.host import Host
from pyinfra.api.inventory import Inventory
from pyinfra.api.operation import add_op
from pyinfra.api.operations import run_ops
from pyinfra.api.state import State
from pyinfra.facts.apk import ApkPackages
from pyinfra.facts.pipx import PipxPackages
from pyinfra.facts.server import LinuxDistribution, LinuxDistributionDict
from pyinfra.facts.server import Command
from pyinfra.operations import apk, files, server
from packaging.version import parse
from pytest import fixture, skip, fail
from pytest_bdd import given, scenario, scenarios, then, when

## GLOBALS AND FIXTURES ~
#

Targets = Literal["ci", "dev", "prod"] 
TARGET: Optional[Targets] = None

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
                    "ssh_strict_host_key_checking": "off",
                    "ssh_known_hosts_file": "/dev/null",
                }
            ))
        case "ci":
            inventory: Inventory = Inventory((
                ["ssh-service"],  # Using localhost instead of ssh-service for CI testing
                {
                    "ssh_user": "root",
                    "ssh_port": 2222,
                    "ssh_password": "xxxxxxxx",
                    "ssh_strict_host_key_checking": "off",
                    "ssh_known_hosts_file": "/dev/null",
                    "ssh_strict_host_key_checking": "off",
                }
            ))
        case "prod":
            fail("Not Implemented")

    state = State(inventory, Config())

    state.print_input = False
    state.print_output = False
    state.print_fact_info = False
    state.print_noop_info = False

    connect_all(state)

    return state


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

@when("target environment is configured for development")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "dev"

@then("the system is configured for development testing")
def _():
    global TARGET
    assert TARGET == "dev"

scenario("deploy.feature", "Target a CI environment for verification")

@when("target environment is configured for continuous integration")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "ci"

@then("the system is configured for CI testing")
def _():
    global TARGET
    assert TARGET == "ci"

scenario("deploy.feature", "Target a production environment for customers")

@when("target environment is configured for production")
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
    add_op(state, apk.packages, packages=["poetry"])
    # Run all operations at the end of the sequence
    run_ops(state)

@then("python version >= 3.12")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert parse(list(packages["python3"])[0]) >= parse("3.12")

@then("nodejs version >= 18")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert parse(list(packages["nodejs"])[0]) >= parse("18")

@then("sqlite version >= 3.48")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert parse(list(packages["sqlite"])[0]) >= parse("3.48")

@then("poetry version >= 1.8")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert parse(list(packages["poetry"])[0]) >= parse("1.8")

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

    add_op(state,
       apk.update
    )
    add_op(state,
       apk.upgrade
    )
    add_op(state, apk.packages, packages=["git", "curl", "libcurl", "python3-dev", "build-base"])
    run_ops(state)

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

    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && poetry lock"
        ],
    )

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

    service: StringIO = StringIO(dedent(
        """
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
        """).strip()
    )

    add_op(
        state,
        files.put,
        src=service,
        dest="/etc/init.d/saleor",
        mode="0755",
    )

@when("Saleor service is enabled")
def _(state: State, deployed: bool):
    if deployed:
        skip()

    add_op(
        state,
        server.shell,
        commands=[
            "rc-update add saleor default",
            "rc-service saleor start || true"
        ],
    )
    run_ops(state)

@then("saleor version >= 3.20")
def _(host: Host):
    # Check saleor version using poetry
    cmd_result = host.get_fact(Command, command="cd /opt/saleor && poetry version | awk '{print $2}' || echo '0.0.0'")
    version = cmd_result.get('stdout', '').strip() if isinstance(cmd_result, dict) else ''
    assert parse(version) >= parse("3.20")

@then("OpenRC manages the running saleor service")
def _(host: Host):
    # Verify service is running and managed by OpenRC
    cmd_result = host.get_fact(Command, command="rc-service saleor status | grep -q 'started' && echo 'running'")
    status = cmd_result.get('stdout', '').strip() if isinstance(cmd_result, dict) else ''
    assert status == "running"

@then("Saleor GraphQL endpoint responds successfully")
def _(host: Host):
    # Test the GraphQL endpoint to see if it's responding
    # Retry up to 3 times with a short delay to handle potential startup delay
    cmd_result = host.get_fact(Command, command="""
    for i in 1 2 3; do
        STATUS=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/graphql/ || echo 'failed')
        if [ "$STATUS" = "200" ] || [ "$STATUS" = "400" ]; then
            echo "$STATUS"
            exit 0
        fi
        sleep 2
    done
    echo "$STATUS"
    """)
    
    status_code = cmd_result.get('stdout', '').strip() if isinstance(cmd_result, dict) else ''
    assert status_code, "No status code returned from curl command"
    assert status_code in ["200", "400"], f"Unexpected status code: {status_code}"  # 400 can occur when sending an empty request, which is still valid
