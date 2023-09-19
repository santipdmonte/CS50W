from django.apps import AppConfig


class ItemTrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'item_track'

    def ready(self):
        import item_track.signals
