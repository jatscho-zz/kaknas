# -*- coding: utf-8 -*-
from os import path

class Config(object):
    DEBUG = False
    TESTING = False
    ROOT_DIR = path.abspath(
        path.dirname(path.join(__file__))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
