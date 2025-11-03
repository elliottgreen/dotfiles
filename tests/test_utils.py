import subprocess
from arch_bootstrap import utils

def test_log_and_command_exists(tmp_path):
    utils.log("message")  # should not raise
    assert utils.command_exists("echo")
    assert not utils.command_exists("definitely_not_a_command")

def test_run_returns_result():
    result = utils.run(["echo", "hi"], capture=True)
    assert result.stdout.strip() in ("hi", "ok")

