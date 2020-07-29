import os
class Config:
    DEBUG=True
class Development(Config):
    DEBUG=True
class Production(Config):
    DEBUG=False
    