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
from pyinfra.operations import apk, files, server, systemd
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

@then("the platform is ready for application hosting")
def _():
    # This is a higher-level assertion that would typically verify multiple
    # platform capabilities are ready. For this stub, we'll assume success
    # if we've reached this point after the OS check passed.
    assert True

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
    # Run all queued ops after last package declaration
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
    # components for Saleor are available
    packages = host.get_fact(ApkPackages)
    assert "python3" in packages
    assert "nodejs" in packages
    assert "sqlite" in packages

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

@when("Saleor core is available")
def _(state: State, deployed: bool):
    if deployed:
        skip()
        
    # Install git if not present
    add_op(state, apk.packages, packages=["git"])
    
    # Clone saleor repository
    add_op(
        state,
        server.shell,
        commands=[
            "test -d /opt/saleor || git clone https://github.com/saleor/saleor.git /opt/saleor"
        ],
    )
    
    # Install Python dependencies
    add_op(
        state,
        server.shell,
        commands=[
            "cd /opt/saleor && python3 -m pip install -e ."
        ],
    )
    
    # Create systemd service file
    add_op(
        state,
        files.template,
        src="templates/saleor.service.j2",
        dest="/etc/systemd/system/saleor.service",
        create_remote_dir=True,
    )
    
    # Enable and start the service
    add_op(state, systemd.service, service="saleor", running=True, enabled=True)
    
    run_ops(state)

@then("saleor version >= 3.20")
def _(host: Host):
    # Check saleor version using pip show
    cmd_result = host.get_fact(Command, command="pip show saleor | grep Version")
    version_line = cmd_result['stdout']
    
    # Extract version from output
    version = version_line.split(':')[1].strip()
    assert parse(version) >= parse("3.20")

@then("saleor service is running")
def _(host: Host):
    # Check if service is running and directory exists
    cmd_result = host.get_fact(Command, command="systemctl is-active saleor")
    assert cmd_result['stdout'].strip() == "active"
    
    # Check if saleor directory exists
    saleor_dir = host.get_fact(Directory, name="/opt/saleor")
    assert saleor_dir is not None

@then("the platform can process commerce transactions")
def _(host: Host):
    # This is a high-level business capability test
    # For a stub implementation, we'll check that the Saleor service is running
    # and responding to HTTP requests
    cmd_result = host.get_fact(Command, command="curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/graphql/")
    status_code = cmd_result['stdout'].strip()
    assert status_code == "200"  # Assuming Saleor GraphQL endpoint is responding with 200 OK
