# -*- coding: utf-8 -*-
import getpass

from password import domain, mvn
from password.jfrog import JFrogApi


def _read_new_password():
    current_password = getpass.getpass('Current password: ')
    new_password = getpass.getpass('New password: ')
    new_password_valid = getpass.getpass('Retype new password: ')
    if new_password != new_password_valid:
        print("Passwords did not match!")
        return current_password, None
    print("")
    return current_password, new_password


class InteractivePassy:

    def __init__(self, api_base_url, maven_settings_xml):
        self.api_base_url = api_base_url
        self.maven_settings_xml = maven_settings_xml
        self.user_name = getpass.getuser()

    def run(self):
        self._print_header()
        current_password, new_password = _read_new_password()
        if new_password is None:
            return

        print("--------------------------- DOMAIN ---------------------------------------------")
        print("Changing domain password using 'vastool'")
        if not domain.change_password(current_password, new_password):
            return
        print("[OK] Domain password has been changed")
        print("--------------------------- MAVEN ----------------------------------------------")
        print("Updating maven settings.xml")
        encrypted_password = JFrogApi(self.api_base_url, self.user_name, new_password).get_encrypted_password()
        mvn.change_password(self.maven_settings_xml, encrypted_password)
        print("[OK] Maven settings.xml has been updated")

    def _print_header(self):
        print(f'''
 _______  _______  _______  _______  __   __ 
|       ||   _   ||       ||       ||  | |  |
|    _  ||  |_|  ||  _____||  _____||  |_|  |
|   |_| ||       || |_____ | |_____ |       |
|    ___||       ||_____  ||_____  ||_     _|
|   |    |   _   | _____| | _____| |  |   |  
|___|    |__| |__||_______||_______|  |___|

! This tool updates your password globally !

Username: {self.user_name}
Artifactory: {self.api_base_url}
Local MVN settings: {self.maven_settings_xml}
'''[1:])
