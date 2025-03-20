import os


ENV = os.getenv("ENVIRONMENT", "production")

if ENV == "production":
    from .production import ProductionSettings as Settings
elif ENV == "development":
    from .development import DevelopmentSettings as Settings
else:
    from .local import LocalSettings as Settings

settings = Settings()
