from django.apps import AppConfig
import os

default_app_config = 'feed.FeedConfig'


def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class FeedConfig(AppConfig):
    name = get_current_app_name(__file__)

    verbose_name = '博客'
