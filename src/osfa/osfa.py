
"""
OSFA -- One Shell For All
"""
VERSION = "1.14"
"""version 1.14"""
from cmd import Cmd
import os, os.path as path
import subprocess
from shutil import rmtree
from sys import platform

from os import system
__all__ = ["CmdSh","RunShell"]
def what_os():
    if platform == "linux" or platform == "linux2":
        return 'Linux'
    elif platform == "darwin":
        return 'Mac'
    elif platform == "win32":
        return 'Windows'
system("title ofsa")
class CmdSh(Cmd):
    @staticmethod
    def _getRealPath(fPath):
        return path.abspath(path.expanduser(path.expandvars(fPath)))
    def do_credits(self, arg):
        """prints the credits"""
        a = 'Created by FreehandBlock51 and SuperPotato9 and released under the MIT license \n'
        self.stdout.write(a)
    def do_hello(self, arg):
            self.stdout.write('hello \n')
            os = what_os()
            if os == 'Windows':
                import win32com.client as wincl
                speak = wincl.Dispatch("SAPI.SpVoice")
                speak.Speak('hello world')
            if os == 'Mac':
                subprocess.run('say hello ', stdin=self.stdin, stdout=self.stdout, stderr=self.stdout, shell=True)
            

    def do_checkos(self, arg):
        '''checks what OS your running'''
        self.stdout.write(what_os() + '\n')
    def do_say(self, arg):
        '''speaks given message'''
        os = what_os()
        if os == 'Windows':
            import win32com.client as wincl
            speak = wincl.Dispatch("SAPI.SpVoice")
            speak.Speak(arg)
        if os == 'Mac':
            subprocess.run('say ' + arg, stdin=self.stdin, stdout=self.stdout, stderr=self.stdout, shell=True)
            
        
        
    def do_title(self, arg):
        """changes current osfa window title note only supported on windows"""
        if what_os() == 'Windows':
            if arg.strip():
                titlestr = ''
                subprocess.run('title ' + arg, stdin=self.stdin, stdout=self.stdout, stderr=self.stdout, shell=True)
            if not arg.strip():
                system("title " + 'ofsa')
        
    def do_moo(self, arg):
        """Prints an image of a cow speaking the given message"""
        if arg == '':
            cow = '''
 
          < moo >
 
             \\  ^__^
              \\ (oo)\\________
                (__)\\        )\\/\\
                     ||----W |
                     ||     ||
'''
        else:
            cow = '''
 
          < {stuff} >
 
             \\  ^__^
              \\ (oo)\\________
                (__)\\        )\\/\\
                     ||----W |
                     ||     ||
'''.format(stuff=arg)
        self.stdout.write(cow)                                                                                                                                                                                                                                                  
    def do_version(self, arg=None):
        """Prints the current version of OSFA"""
        self.stdout.write("OSFA version " + VERSION + '\n')
    def do_echo(self, arg):
        """Prints text to the screen"""
        self.stdout.write(arg + '\n')
    def do_exit(self, *args):
        """Exits osfa"""
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
            self.stdout.write("Command failed with exception:\n" + str(e) + '\n')
        finally:
            self.stdout.write("{END DEBUG}\n")
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
            subprocess.run(cmdString, stdin=self.stdin, stdout=self.stdout, stderr=self.stdout, shell=True)
        except OSError:
            self.stdout.write("Couldn't start from shell, attempting to run as process...\n")
            try:
                subprocess.run(cmdString, stdin=self.stdin, stdout=self.stdout, stderr=self.stdout)
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
                self.stdout.write("Can't decode non-unicode characters in a file!\n")
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
        
    intro = """OSFA: One Shell For All
Version {}""".format(VERSION)
    endprompt = "(OSFA) "
    @property
    def prompt(self):
        return "{} {}".format(os.getcwd(), self.endprompt)
    title = "OSFA"

def RunShell():
    """Starts a shell.
    Called when script is executed by the command line"""
    cmdsh = CmdSh()

    try:
        while True:
            try:
                cmdsh.cmdloop()
                break
            except KeyboardInterrupt:
                print()
                cmdsh.intro = None
    except Exception as e:
        input("\nfatal shell error:\n{}\n press <ENTER> to exit...".format(e))

if __name__ == "__main__":
    RunShell()
