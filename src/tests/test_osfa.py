import pytest
from osfa import CmdSh, RunShell, VERSION
from random import randint
from sys import argv

def _prevent_timeout(piped_cmdsh):
    """Prevent OSFA from hanging on
    tests by adding the 'exit' command
    to its stdin stream"""
    piped_cmdsh.stdin.writelines(["exit"])
    piped_cmdsh.stdin.seek(0)

def testCmdQueue(piped_cmdsh):
    piped_cmdsh.cmdqueue = [
        "echo hello!"
    ]
    _prevent_timeout(piped_cmdsh)
    piped_cmdsh.cmdloop()
    piped_cmdsh.stdout.seek(0)
    output = piped_cmdsh.stdout.read()
    assert output.count("hello!") > 0

def testBatchExec(tmp_path, piped_cmdsh):
    tFile = tmp_path / ('./' + str(randint(-99999, 999999)) + ".tmp") # randomize name so we don't accidently conflict
    tFile.write_text("""echo hello!
version""")
    _prevent_timeout(piped_cmdsh)
    RunShell(argv=(argv[0], str(tFile)), cmdsh=piped_cmdsh)
    piped_cmdsh.stdout.seek(0)
    output = piped_cmdsh.stdout.read()
    assert output.count("hello!") > 0 and output.count(VERSION) > 1


def testExecCommand(tmp_path, piped_cmdsh):
    tFile = tmp_path / "execTest.tmp"
    tFile.write_text("""
    echo hello!
    exit
    """)
    piped_cmdsh.cmdqueue = [
        "exec " + str(tFile)
    ]
    _prevent_timeout(piped_cmdsh)
    piped_cmdsh.cmdloop()
    piped_cmdsh.stdout.seek(0)
    output = piped_cmdsh.stdout.read()
    assert output.count("hello!") > 0
