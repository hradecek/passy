# -*- coding: utf-8 -*-
import json
import logging
import requests
from requests.auth import HTTPBasicAuth

from exceptions import UpdatePasswordException

API = '/api'
API_SECURITY = f'{API}/security'

API_HEADERS = {
    'Content-Type': 'application/json',
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class JFrogApi:
    """
    Invokes JFrog REST API.
    """

    def __init__(self, base_url, user_name, password):
        self.base_url = base_url
        self.user_name = user_name
        self.password = password

    def change_password(self, new_password):
        """Change password for current user.

        :param str new_password: new password
        :raise: UpdatePasswordException if password cannot be updated
        :return: encrypted new password if old password has been changed successfully
        """
        change_password_url = f'{self.base_url}{API_SECURITY}/users/authorization/changePassword'
        payload = {
            'userName': self.user_name,
            'oldPassword': self.password,
            'newPassword1': new_password,
            'newPassword2': new_password
        }

        logger.info("Sending POST request to %s", change_password_url)
        changed_password_response = requests.post(change_password_url,
                                                  auth=HTTPBasicAuth(self.user_name, self.password),
                                                  headers=API_HEADERS,
                                                  data=json.dumps(payload))
        check_response(changed_password_response)

        encrypted_password_response = self.get_encrypted_password()
        self.password = new_password

        return encrypted_password_response.content

    def get_encrypted_password(self):
        encrypted_password_url = f'{self.base_url}{API_SECURITY}/encryptedPassword'
        logger.info("Sending GET request to %s: %s", encrypted_password_url)
        encrypted_password_response = requests.get(encrypted_password_url,
                                                   auth=HTTPBasicAuth(self.user_name, self.password))
        logger.info("Response '%s'", str(encrypted_password_response))
        check_response(encrypted_password_response)

        return encrypted_password_response.content.decode('utf-8')


def check_response(response):
    try:
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as err:
        raise UpdatePasswordException(err.response.content.decode('utf-8'))
