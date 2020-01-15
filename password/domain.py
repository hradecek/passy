# -*- coding: utf-8 -*-
import logging
import subprocess

VASTOOL_BIN = '/opt/quest/bin/vastool'

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def change_password(current_password, new_password):
    """Change current user's domain password using vastool

    :param str current_password: current password
    :param str new_password: new password
    :return: True if password has been changed successfully, False otherwise
    """
    logger.info("Calling vastool passwd")
    return _run_expect(current_password, new_password)


# TODO: Pexpect?
def _run_expect(current_password, new_password):
    domain_name = _vastool_get_kerberos_id()
    expect_program = f'''
spawn {VASTOOL_BIN} -w "{current_password}" passwd
expect "New password for {domain_name}:"
send -- "{new_password}\r"
expect "Verify password - New password for {domain_name}:"
send -- "{new_password}\r"
expect eof
'''.strip()
    output = subprocess.run(['expect', '-c', expect_program], capture_output=True).stdout.decode('utf-8')
    print(output)
    return False if "ERROR" in output else True


def _vastool_get_kerberos_id():
    vastool_info = subprocess.run([VASTOOL_BIN, "info", "id"], capture_output=True).stdout.decode('utf-8')
    return vastool_info.splitlines()[0].split(':')[1].strip()

