from django.conf import settings

__all__ = ["mastrms_apps"]


def mastrms_apps():
    "returns a list of installed mastrms django apps"
    return [t.split('.', 1)[-1] for t in settings.INSTALLED_APPS if t.startswith('mastrms.')]
