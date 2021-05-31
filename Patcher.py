import os
import ctypes
import subprocess
import sys
import win32net
global versionstr
versionstr = ""
global version
version = ""
latest = "39813c0600000f84e16a0100"
v2004 = "39813c0600000f84d9510100"
v1909or1903 = "39813c0600000f845d610100"
v1809 = "39813c0600000f843b2b0100"
v1803 = "8b993c0600008bb938060000"
v1709 = "39813c0600000f84b17d0200"
patch = "b80001000089813806000090"
username = os.getenv('username')
documents_dir = 'C:\\Users\\' + username + "\\" + "Documents"
choice = input("This tool modifies a core Windows dll,proceeding could be dangerous for your system do you wish to continue ? (y/n) > ")
if choice == "n":
    print("Exiting ....")
    exit()
elif choice == "y":
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin == False:
        print("You need to be admin for this operation")
        print("Exiting....")
        exit()
    else:
        if 1 == 1:
            class disable_fsr():
                disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
                revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
                def __enter__(self):
                    self.old_value = ctypes.c_long()
                    self.success = self.disable(ctypes.byref(self.old_value))
                def __exit__(self, type, value, traceback):
                    if self.success:
                        self.revert(self.old_value)
        with disable_fsr():
            with open('C:/Windows/System32/termsrv.dll', 'rb') as f:
                content = f.read().hex()
            if latest in content:
                version += latest
                versionstr += "version latest"
            elif v2004 in content:
                version += v2004
                versionstr += "version 2004"
            elif v1909or1903 in content:
                version += v1909or1903
                versionstr += "version 1909 or 1903"
            elif v1809 in content:
                version += v1809
                versionstr += "version 1809"
            elif v1803 in content:
                version += v1803
                versionstr += "version 1803"
            elif v1709 in content:
                version += v1709
                versionstr += "version 1709"
            else:
                print("[!] Windows version not supported or already patched aborting...")
                exit()
            if 'logonserver' in os.environ:
                server = os.environ['logonserver'][2:]
            else:
                server = None
            groups = win32net.NetUserGetLocalGroups(server, os.getlogin())
            isadmin = False
            for group in groups:
                if group.lower().startswith('admin'):
                    isadmin = True
                    admingroup = group
            print('[*] Windows ' + versionstr + ' detected')
            print("[*] Making backup to " + documents_dir + "\\backup_termsrv.dll")
            os.system("copy C:\\Windows\\System32\\termsrv.dll " + documents_dir + "\\" + "backup_termsrv.dll>nul")
            print("[*] Taking ownership of termsrv file...")
            os.system("takeown /F C:\\Windows\\System32\\termsrv.dll /A>nul")
            os.system("icacls C:\\Windows\\System32\\termsrv.dll /grant " + admingroup + ":F>nul")
            print("[*] Stopping Remote Desktop service....")
            def STOP():
                import subprocess
                subprocess = subprocess.Popen('taskkill /F /FI "SERVICES eq TermService"', shell=True, stdout=subprocess.PIPE)
                subprocess_return = subprocess.stdout.read()
                if "No tasks running" not in str(subprocess_return): 
                    STOP()    
            STOP()
            os.system("net stop TermService /y>nul")
            print("[*] Patching file...")
            content = content.replace(version, patch)
            with open('C:/Windows/System32/termsrv.dll', 'wb') as f:
                f.write(bytes.fromhex(content))
            print("[*] Restarting TermService")
            os.system("net start TermService>nul")
            print("[*] Successful\n[*] now exiting...")
else:
    print("Input not recognized")

