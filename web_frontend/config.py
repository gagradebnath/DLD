"""
Application Configuration
"""

import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dld_ic_library_2025')
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
