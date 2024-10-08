"""Test installation configuration of puppet module."""

import pytest

from tests.integration_tests.instances import IntegrationInstance
from tests.integration_tests.util import verify_clean_boot, verify_clean_log

SERVICE_DATA = """\
#cloud-config
puppet:
  install: true
  install_type: packages
"""


@pytest.mark.user_data(SERVICE_DATA)
def test_puppet_service(client: IntegrationInstance):
    """Basic test that puppet gets installed and runs."""
    log = client.read_from_file("/var/log/cloud-init.log")
    verify_clean_log(log)
    verify_clean_boot(client)
    puppet_ok = client.execute("systemctl is-active puppet.service").ok
    puppet_agent_ok = client.execute(
        "systemctl is-active puppet-agent.service"
    ).ok
    assert True in [puppet_ok, puppet_agent_ok]
    assert False in [puppet_ok, puppet_agent_ok]
    assert "Running command ['puppet', 'agent'" not in log


EXEC_DATA = """\
#cloud-config
puppet:
  install: true
  install_type: packages
  exec: true
  exec_args: ['--noop']
"""


@pytest.mark.user_data
@pytest.mark.user_data(EXEC_DATA)
def test_puppet_exec(client: IntegrationInstance):
    """Basic test that puppet gets installed and runs."""
    log = client.read_from_file("/var/log/cloud-init.log")
    assert "Running command ['puppet', 'agent', '--noop']" in log
