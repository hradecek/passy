# -*- coding: utf-8 -*-
from config import ConfigReader
from interactive import InteractivePassy


class PasswordUpdateError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


# Run IT!
if __name__ == '__main__':
    config = ConfigReader()
    InteractivePassy(config.artifactory_url(), config.maven_settings_xml()).run()
