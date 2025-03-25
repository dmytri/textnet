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
from pyinfra.facts.openrc import OpenrcEnabled
from pyinfra.facts.server import LinuxDistribution, LinuxDistributionDict, Command
from pyinfra.operations import apk, openrc, files, server, postgresql, postgres
from packaging.version import parse
from pytest import fixture, skip, fail
from pytest_bdd import scenario, scenarios, then, when

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

## SCENARIOS ~
#

scenarios("deploy.feature")

## PREFLIGHT SCENARIOS
#

scenario("deploy.feature", "TND Target a development environment for testing")

@when("TNDE the target environment is configured for development")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "dev"

@then("TNDC the system is configured for development testing")
def _():
    global TARGET
    assert TARGET == "dev"

scenario("deploy.feature", "TNC Target a CI environment for verification")

@when("TNCE the target environment is configured for continuous integration")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "ci"

@then("TNCC the system is configured for CI testing")
def _():
    global TARGET
    assert TARGET == "ci"

scenario("deploy.feature", "TNP Target a production environment for customers")

@when("TNPE the target environment is configured for production")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "prod"

@then("TNPC the system is configured for production use")
def _():
    global TARGET
    assert TARGET == "prod"

## DEPLOY SCENARIOS ~
#

scenario("deploy.feature", "TNA Provide a stable Alpine Linux platform")

@when("TNAU the system packages up to date")
def _(state: State):
    run_ops(state)

@then("TNAA OS Alpine Linux 3.21")
def _(host: Host):
    distro: LinuxDistributionDict = host.get_fact(LinuxDistribution)
    assert distro["release_meta"]["PRETTY_NAME"] == "Alpine Linux v3.21"

scenario("deploy.feature", "TNR Enable required runtime environments for Saleor")

@when("TNRA Python runtime is available")
def _(state: State):
    add_op(state, apk.packages, packages=["python3"])

@when("TNRB NodeJS runtime is available")
def _(state: State):
    add_op(state, apk.packages, packages=["nodejs"])

@when("TNRC PostgreSQL database is available")
def _(state: State):
    add_op(state, apk.packages, packages=["postgresql", "postgresql-contrib"])

@when("TNRS PostgreSQL service is enabled")
def _(state: State):
    add_op(state, openrc.service, "postgresql", running=True, enabled=True)

@when("TNRD Poetry is available")
def _(state: State):
    add_op(state, apk.packages, packages=["poetry"])

@then("TNRX Host has converged")
def _(state: State):
    run_ops(state)

@then("TNRE python version >= 3.12")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["python3"])[0]) >= parse("3.12")

@then("TNRF nodejs version >= 18")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["nodejs"])[0]) >= parse("18")

@then("TNRG postgresql version >= 17")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["postgresql17"])[0]) >= parse("17")

@then("TNRI PostgreSQL service is operational")
def _(host: Host):
    services: dict = host.get_fact(OpenrcEnabled, runlevel="defualt")
    assert "postgresql" in services

@then("TNRH poetry version >= 1.8")
def _(host: Host):
    packages: dict = host.get_fact(ApkPackages)
    assert parse(list(packages["poetry"])[0]) >= parse("1.8")

scenario("deploy.feature", "TNS Provide Saleor commerce capabilities")

@when("TNSB build tools are available") # was SCF1
def _(state: State):
    add_op(
        state,
        apk.update)
    add_op(state, apk.upgrade)
    add_op(
        state,
        apk.packages,
        packages=[
            "git",
            "curl",
            "curl-dev",
            "libcurl",
            "python3-dev",
            "py3-virtualenv",
            "build-base",
            "musl-dev",
            "linux-headers",
        ],
    )

@when("TNSU PostgreSQL database is setup")
def _(state: State):
    add_op(state, server.user,
        user='postgres',
        password='xxxxxxxx'
    )
    add_op(state, postgres.role,
        pgsql_user="postgres",
        pgsql_password="xxxxxxxx",
        role="saleor",
        password="saleor",
    )
    add_op(state, postgresql.database,
        pgsql_user="postgres",
        pgsql_password="xxxxxxxx",
        database="saleor",
        owner="saleor",
    )

@when("TNSS Saleor source code is available") # was SCF2
def _(state: State):
    add_op(
        state,
        server.shell,
        commands=[
            "test -d /opt/saleor || git clone https://github.com/saleor/saleor.git /opt/saleor"
        ]
    )

@when("TNSN Saleor Python virtual environment is available") # was SCF3
def _(state: State):
    # Create a virtual environment for Saleor
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && python3 -m virtualenv .venv"
        ],
    )

@when("TNSD Saleor Python dependencies are installed") # was SCF4
def _(state: State):
    # Use the virtual environment for poetry operations
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && .venv/bin/pip install --upgrade pip"
        ],
    )

    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && .venv/bin/pip install poetry"
        ],
    )

    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && .venv/bin/poetry lock"
        ],
    )

    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && .venv/bin/poetry install"
        ],
    )

@when("TNSP Saleor service definition is present") # was SCF5
def _(state: State):
    service: StringIO = StringIO(dedent(
        """
        #!/sbin/openrc-run

        name="Saleor Commerce Platform"
        description="Saleor API and commerce services"
        supervisor=supervise-daemon
        command="/opt/saleor/.venv/bin/poetry"
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

@when("TNSE Saleor service is enabled") # was SCF6
def _(state: State):
    add_op(
        state,
        server.shell,
        commands=[
            "rc-update add saleor default",
            "rc-service saleor start || true"
        ],
    )

@when("TNSX Host has converged") # was SCF6
def _(state: State):
    run_ops(state)

@then("TNSV saleor version >= 3.20") # was SCF7
def _(host: Host):
    # Check saleor version using poetry
    cmd_result = host.get_fact(Command, command="cd /opt/saleor && poetry version | awk '{print $2}' || echo '0.0.0'")
    version = cmd_result.get('stdout', '').strip() if isinstance(cmd_result, dict) else ''
    assert parse(version) >= parse("3.20")

@then("TNSO OpenRC manages the running saleor service")
def _(host: Host):
    service_status = host.get_fact(OpenrcEnabled, service="saleor")
    assert service_status == "started", "Saleor service is not running"

@then("TNSG Saleor GraphQL endpoint responds successfully") # was SCF9
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
