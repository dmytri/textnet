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
from pyinfra.facts.files import Directory
from pyinfra.facts.openrc import OpenrcEnabled
from pyinfra.facts.server import LinuxDistribution, LinuxDistributionDict
from pyinfra.operations import apk, git, pip, openrc, files, server, postgres, npm
from packaging.version import parse
from pytest import fixture, fail, skip
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

    match TARGET:
        case "dev":
            state.print_input = False
            state.print_output = False
            state.print_fact_info = False
            state.print_noop_info = False
        case _:
            state.print_input = True
            state.print_output = True
            state.print_fact_info = True
            state.print_noop_info = True

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
    add_op(state, apk.update)
    add_op(state, apk.upgrade)
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

@when("TNSB build tools are available")
def _(state: State):
    add_op(
        state,
        apk.update)
    add_op(state, apk.upgrade)
    add_op(
        state,
        apk.packages,
        packages=[
            "shadow",
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

@when("TNSU Saleor database is setup")
def _(state: State):
    add_op(state, server.user,
        user='postgres',
        password='xxxxxxx'
    )

    add_op(state, postgres.role,
        psql_user="postgres",
        psql_password="xxxxxxxx",
        role="saleor",
        password="saleor",
        superuser=True
    )

    add_op(state, postgres.database,
        psql_user="postgres",
        psql_password="xxxxxxxx",
        database="saleor",
        owner="postgres"
    )

@when("TNSS Saleor source code is available")
def _(state: State, host: Host):
    if not host.get_fact(Directory, path="/opt/saleor"):
        add_op(
            state,
            git.repo,
            src="https://github.com/saleor/saleor.git",
            dest="/opt/saleor",
            branch="main"
        )

@when("TNSN Saleor Python virtual environment is available")
def _(state: State):
    add_op(
        state,
        pip.venv,
        name="Create a virtualenv",
        path="/opt/saleor/.venv"
    )

@when("TNSD Saleor Python dependencies are installed")
def _(state: State):
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && .venv/bin/pip show poetry || ("
            ".venv/bin/pip install --upgrade pip"
            " && .venv/bin/pip install poetry"
            " && .venv/bin/poetry lock"
            " && .venv/bin/poetry install"
            " && .venv/bin/poetry run python manage.py migrate"
            " && .venv/bin/poetry run python manage.py createsuperuser"
            ")"
        ]
    )

@when("TNSP Saleor service definition is present")
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
        export API_URI="http://localhost:8000/graphql/"

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

@when("TNSE Saleor service is enabled")
def _(state: State, host: Host):
    add_op(state, openrc.service, "saleor", running=True, enabled=True)

@then("TNSX Host has converged")
def _(state: State):
    run_ops(state)

@then("TNSV Saleor is operational")
def _(host: Host):
    services: dict = host.get_fact(OpenrcEnabled, runlevel="defualt")
    assert "saleor" in services

scenario("deploy.feature", "TNI Ensure Saleor Dashboard Dependencies are Installed")

@when("TNIB build tools are available")
def _(state: State):
    add_op(
        state,
        apk.update)
    add_op(state, apk.upgrade)
    add_op(
        state,
        apk.packages,
        packages=[
            "nodejs",
            "npm"
        ],
    )

@when("TNIS Saleor Dashboard source code is available")
def _(state: State, host: Host):
    if not host.get_fact(Directory, path="/opt/saleor-dashboard"):
        add_op(
            state,
            git.repo,
            src="https://github.com/saleor/saleor-dashboard.git",
            dest="/opt/saleor-dashboard",
            branch="3.20.33"
        )

@when("TNID Saleor dashboard dependencies are installed")
def _(state: State):
    # Install serve globally
    add_op(
        state,
        npm.packages,
        packages=["serve"],
        directory=None,  # Install globally
    )
    
    # Install dashboard dependencies and build
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor-dashboard"
            " && export CI=1"
            " && export API_URL=http://localhost:8000/graphql/"
            " && export APP_MOUNT_URI=/dashboard/"
            " && export STATIC_URL=/dashboard/"
            " && npm install --legacy-peer-deps"
            " && npm run build"
        ]
    )

@then("TNIX Host has converged")
def _(state: State):
    run_ops(state)

scenario("deploy.feature", "TNB Provide Saleor Dashboard")

@when("TNBP Saleor Dashboad service definition is present")
def _(state: State):
    service: StringIO = StringIO(dedent(
        """
        #!/sbin/openrc-run

        name="Saleor Dashboard"
        description="Saleor Dashboard web interface"
        supervisor=supervise-daemon
        command="/usr/bin/serve"
        command_args="-s -l 9000 build"
        directory="/opt/saleor-dashboard"
        pidfile="/run/saleor-dashboard.pid"
        output_log="/var/log/saleor-dashboard.log"
        error_log="/var/log/saleor-dashboard.err"
        export API_URL="http://localhost:8000/graphql/"
        export APP_MOUNT_URI="/dashboard/"
        export STATIC_URL="/dashboard/"

        depend() {
            need net
            after firewall
            after saleor
        }
        """).strip()
    )

    add_op(
        state,
        files.put,
        src=service,
        dest="/etc/init.d/saleor-dashboard",
        mode="0755",
    )

@when("TNBE Saleor Dashboard service is enabled")
def _(state: State):
    add_op(state, openrc.service, "saleor-dashboard", running=True, enabled=True)

@then("TNBX Host has converged")
def _(state: State):
    run_ops(state)

@then("TNBV Saleor Dashboad is operational")
def _(host: Host):
    services: dict = host.get_fact(OpenrcEnabled, runlevel="defualt")
    assert "saleor-dashboard" in services
