import pytest, os

@pytest.fixture()#scope="session")
def piped_cmdsh():
    from osfa import CmdSh
    from io import StringIO
    piped_cmdsh = CmdSh(stdin=StringIO(""), stdout=StringIO(""))
    piped_cmdsh.use_rawinput = False
    return piped_cmdsh