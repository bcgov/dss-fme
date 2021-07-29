import json
import os
import win32con
import win32security


class WinUtil:
    """ A class that enable impersonation on Windows"""
    """ 1. Create object: WinUtil("david") """
    """ 2. open() """
    """ 3. execute your file operation """
    """ 4. close(), with try-finlly """
    """ created and tested on Python 3.9 """

    # this file contains impersonation account settings
    SECRET_CONFIG = "secret.json"

    """ specify the username of the impersonation """
    def __init__(self, imperson_name):
        self.on = False
        with open(self.SECRET_CONFIG) as secrect_config_json:
            secrect_config = json.load(secrect_config_json)
        self.password = None
        self.domain = None
        for acc in secrect_config["account"]:
            if acc["user"] == imperson_name:
                self.user = acc["user"]
                self.password = acc["password"]
                self.domain = acc["domain"]
                break
        if not self.password:
            raise Exception("Imperson configration error.")
        """ if domain not provided, use the current """
        if not self.domain:
            self.domain = os.environ['userdomain']

    def __del__(self):
        self.close()

    def open(self):
        self.handle = win32security.LogonUser(self.user, self.domain,
                                              self.password, win32con.LOGON32_LOGON_INTERACTIVE,
                                              win32con.LOGON32_PROVIDER_DEFAULT)
        win32security.ImpersonateLoggedOnUser(self.handle)
        self.on = True

    def close(self):
        if not self.on:
            return
        win32security.RevertToSelf()  # terminates impersonation
        self.handle.Close()  # guarantees cleanup
