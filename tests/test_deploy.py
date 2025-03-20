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
from pyinfra.operations import apk
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

scenario("deploy.feature", "Target environment is set to dev")

@when("set target environment to dev")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "dev"

scenario("deploy.feature", "Target environment is set to ci")

@when("set target environment to ci")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "ci"

scenario("deploy.feature", "Target environment is set to prod")

@when("set target environment to prod")
def _():
    global TARGET
    assert TARGET is None
    TARGET = "prod"

## DEPLOY SCENARIOS ~
#

scenario("deploy.feature", "Ensure Alpine Linux 3.21 with required packages")

@when("system packages up to date")  # Changed Given->When since it has side effects
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

scenario("deploy.feature", "Ensure Saleor Dependencies Are Installed")

@when("python installed")
def _(state: State, deployed: bool):
    if deployed:
        skip()
    add_op(state, apk.packages, packages=["python3"])

@when("nodejs installed") 
def _(state: State, deployed: bool):
    if deployed:
        skip()
    add_op(state, apk.packages, packages=["nodejs"])

@when("sqlite installed")
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

@then("sqlite version >= 3.49.1")
def _(host: Host):
    packages = host.get_fact(ApkPackages)
    assert "sqlite" in packages
    pkg_version = packages["sqlite"]
    if isinstance(pkg_version, set):
        pkg_version = list(pkg_version)[0]
    assert parse(pkg_version) >= parse("3.49.1")

