# -*- coding: utf-8 -*-
class UpdatePasswordException(Exception):

    def __init__(self, message):
        self.message = message
