# -*- coding: utf-8 -*-
import configparser

CONFIG_KEY = 'config'
ARTIFACTORY_URL = 'ArtifactoryUrl'
MAVEN_SETTINGS_XML = 'MavenSettingsXml'


class ConfigReader:

    def __init__(self, config_path='config.ini'):
        config_reader = configparser.ConfigParser()
        config_reader.read(config_path)
        self.config = config_reader[CONFIG_KEY]

    def artifactory_url(self):
        return self.config[ARTIFACTORY_URL]

    def maven_settings_xml(self):
        return self.config[MAVEN_SETTINGS_XML]
