# -*- coding: utf-8 -*-
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

NAMESPACES = {'settings': 'http://maven.apache.org/SETTINGS/1.1.0'}
PASSWORD_XPATH = './/settings:password'


def change_password(settings_xml_path, password):
    """Update password in maven's settings.xml

    :param str settings_xml_path: path to settings.xml
    :param str password: encrypted password
    """
    logging.info("Updating '%s'", settings_xml_path)
    ET.register_namespace('', 'http://maven.apache.org/SETTINGS/1.1.0')
    tree = ET.parse(settings_xml_path)
    for password_tag in tree.getroot().findall(PASSWORD_XPATH, NAMESPACES):
        password_tag.text = password
    logging.info("Replaced all <password /> text by '%s'", password)
    tree.write(settings_xml_path)
    logging.info("Saving modified '%s'", settings_xml_path)
