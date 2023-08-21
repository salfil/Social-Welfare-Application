from django.apps import AppConfig
  
#defines the configuration of this django application with the configuration settings
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
