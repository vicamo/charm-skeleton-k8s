import logging
from pathlib import Path

import pytest
import yaml


log = logging.getLogger(__name__)
meta = yaml.safe_load(Path("metadata.yaml").read_text())


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test):
    """Test build and deploy."""
    charm = await ops_test.build_charm(".")
    await ops_test.model.deploy(charm)
    await ops_test.model.wait_for_idle(wait_for_active=True, timeout=60 * 60)


async def test_status(ops_test):
    """Check status of deployed application."""
    app = ops_test.model.applications[meta.name]
    assert app.units[0].workload_status == "active"
