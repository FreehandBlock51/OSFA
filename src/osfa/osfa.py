#!/usr/bin/env python

"""
OSFA -- One Shell For All
"""

from cmd import Cmd
import os
import os.path as path
import subprocess
from shutil import rmtree
from sys import argv

__all__ = ["CmdSh", "RunShell", "VERSION"]
VERSION = "2.0"


class CmdSh(Cmd):
    @staticmethod
    def _getRealPath(fPath):
        return path.abspath(path.expanduser(path.expandvars(fPath)))

    def do_moo(self, arg):
        """Prints an image of a cow speaking the given message"""
        if arg == '':
            cow = """
 
          < moo >
 
             \\  ^__^
              \\ (oo)\\________
                (__)\\        )\\/\\
                     ||----W |
                     ||     ||
"""
        else:
            cow = """
 
          < {stuff} >
 
             \\  ^__^
              \\ (oo)\\________
                (__)\\        )\\/\\
                     ||----W |
                     ||     ||
""".format(stuff=arg)
        self.stdout.write(cow)

    def do_version(self, arg=None):
        """Prints the version of OSFA"""
        self.stdout.write("OSFA version " + VERSION + '\n')

    def do_echo(self, arg):
        """Prints text to the screen"""
        self.stdout.write(arg + '\n')

    def do_exit(self, *args):
        """Exits the terminal"""
        return True

    def do_cd(self, newDir="."):
        """Changes the current working directory to the specified one (default '.') and prints it to the screen"""
        newPath = self._getRealPath(newDir)
        try:
            os.chdir(newPath)
            self.stdout.write("Changed to " + newPath + "\n")
        except OSError as e:
            self.stdout.write(e.strerror + "\n")

    def do_lst(self, lDir="."):
        """Lists the contents of a directory"""
        LDir = self._getRealPath(lDir)
        dirs = os.scandir(LDir)
        self.stdout.write("Contents of Directory '" + LDir + "':\n")
        for dirEntry in dirs:
            self.stdout.write('[' + str("file" if dirEntry.is_file() else
                                        "dir " if dirEntry.is_dir() else
                                        "link" if dirEntry.is_symlink() else
                                        "??? ") + '] ' + dirEntry.name + "\n")

    def do_debug(self, command):
        """Debugs a command"""
        self.stdout.write("{DEBUGGING COMMAND '" + command + "'}\n")
        try:
            self.onecmd(command)
        except Exception as e:
            self.stdout.write(
                "Command failed with exception:\n" + str(e) + '\n')
        finally:
            self.stdout.write("{END DEBUG}\n")

    def do_exec(self, file):
        """Runs commands from the specified file, 1 command per line."""
        with open(file, 'r') as cFh:
            oldQueue = self.cmdqueue[:]  # save old queue
            self.cmdqueue = cFh.readlines()
            self.cmdqueue.extend(oldQueue)

    def do_shell(self, command):
        """Attempts to run the given command specified by \
the first argument in a subshell (or as an executable if \
no subshell exists), with the rest of the arguments passed \
as arguments."""
        if command[0] == '"':
            pEnd = command[1:].find('"')
            cmdString = [command[1:pEnd], *command[pEnd+1:].trim().split(' ')]
        else:
            cmdString = command.split(' ')
        try:
            subprocess.run(cmdString, stdin=self.stdin,
                           stdout=self.stdout, stderr=self.stdout, shell=True)
        except OSError:
            self.stdout.write(
                "Couldn't start from shell, attempting to run as process...\n")
            try:
                subprocess.run(cmdString, stdin=self.stdin,
                               stdout=self.stdout, stderr=self.stdout)
            except OSError as e:
                self.stdout.write("Error starting process:\n" + str(e) + '\n')

    def do_readfile(self, file):
        """Outputs the contents of a given file to the shell"""
        rFile = self._getRealPath(file)
        if not path.exists(rFile):
            return
        with open(rFile, 'r') as fd:
            try:
                self.stdout.write("{}\n".format(fd.read()))
            except UnicodeDecodeError:
                self.stdout.write(
                    "Can't decode non-unicode characters in a file!\n")

    def do_pipefile(self, args):
        """Pipes the output of a command to a specified file, listed first.
The file will be overwritten."""
        e = None
        oStdout = self.stdout
        if args[0] == '"':
            file = args[1:args.rfind('"')]
            command = args[len(file) + 2:]
        else:
            argv = args.split(' ')
            file = argv[0]
            command = ' '.join(argv[1:])
        try:
            self.stdout = open(file, 'w')
        except FileNotFoundError:
            oStdout.write("File not found")
        try:
            self.onecmd(command)
        except Exception as ex:
            e = ex
        finally:
            self.stdout.close()
            self.stdout = oStdout
        if e:
            raise e

    def do_erasefile(self, file):
        """Deletes a file."""
        os.remove(self._getRealPath(file))

    def do_erasedir(self, dirPath):
        """Deletes a directory."""
        rmtree(self._getRealPath(dirPath))

    def do_createdir(self, dirPath):
        """Creates a directory."""
        os.mkdir(self._getRealPath(dirPath))

    def do_createfile(self, file):
        """Creates a file."""
        fd = open(self._getRealPath(file), 'x')
        fd.close()

    def do_EOF(self, arg=None):
        """Called when an End-Of-File (Manually triggered by ^D or ^Z+<Enter> on Windows) is given."""
        return self.do_exit()

    def emptyline(self):
        """Called when the input is an empty line.  Overridden from Cmd.emptyline()"""
        pass  # we don't want anything to happen

    intro = """OSFA: One Shell For All
Version {}""".format(VERSION)
    endprompt = "(OSFA) ⁞ "

    @property
    def prompt(self):
        return "⌠{}⌡\n\t{}".format(os.getcwd(), self.endprompt)
    title = "OSFA"


def RunShell(argv=argv, cmdsh=CmdSh()):
    """Starts a shell.
    Called when script is executed by the command line.
    'argv' is arguments passed to the shell, and defaults
    to sys.argv.  'cmdsh' is the shell that will be used,
    and a custom value should only be given for testing."""

    if len(argv) > 1:  # we are given arguments
        file = argv[1]  # interpret first argument as a file
        # TODO if other arguments are parsed, implement flags to differentiate
        cmdsh.cmdqueue = [
            'exec ' + file,
            'exit'
        ]

    try:
        cmdsh.cmdloop()
    except Exception as e:
        input("\nfatal shell error:\n{}\n press <ENTER> to exit...".format(e))


if __name__ == "__main__":
    RunShell()
