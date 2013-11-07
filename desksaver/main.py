#! /usr/bin/env python

from base64 import b64decode
from datetime import timedelta
import os, os.path

from scxrapper.instruments import Scraper, Pattern
from scxrapper.instruments.pages.cached import FilesystemCachedPage, BinaryFile
from scxrapper.instruments.patterns.navigation import AnchorTagPattern
from scxrapper.instruments.mixins import FailFastMixin
from scxrapper.core.actions import action

from configuration import get_config

config, IMAGE_STORAGE_HANDLER = get_config()

class WallbaseScraper(Scraper):
    # default_logging_level = 20
    variables = {
        'tracked_wallpapers': [],
    }

    max_attempt_limit = 1
    error = None

    sub_instruments = ['HomePage']

    @action('end')
    def remove_unvisited_wallpapers(self, logger, **kwargs):
        """ Inspects files in the storage location to find and delete any that aren't current. """

        if self.state.error:
            logger.warn("Fail-fast error detected. Stale wallpaper detection will be skipped.")
            return

        folder = IMAGE_STORAGE_HANDLER.CACHE_LOCATION
        stale = []
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if os.path.isfile(path) and not filename.startswith('.') \
                    and filename not in self.variables['tracked_wallpapers']:
                stale.append(filename)
                logger.warn("Removing unvisited stale wallpaper %r", filename)
                os.remove(path)

        if not len(stale):
            logger.info("No stale wallpapers to remove from %r", folder)

class HomePage(FailFastMixin, FilesystemCachedPage):
    uri = config['uri']
    shelf_life = timedelta(days=1)

    variables = config

    class WallpaperLink(AnchorTagPattern):
        variables = {
            'attributes': {
                'href': r'http://wallbase\.cc/wallpaper/\d+',
            },
        }
        save_variables = {
            'href': "WALLPAPER_PAGE_URL",
        }
        sub_instruments = ['WallpaperDetailPage']

    sub_instruments = [WallpaperLink]

    @action('fail')
    def register_failure(self, **kwargs):
        self.get_root_instrument().state.error = True


class WallpaperDetailPage(FailFastMixin, FilesystemCachedPage):
    uri = "{WALLPAPER_PAGE_URL}"
    shelf_life = timedelta(days=1)

    class WallpaperImageLink(Pattern):
        pattern = r"'\+B\('(?P<data>[^)]+)'\)\+'"
        save_variables = {
            'data': lambda value: {'WALLPAPER_URL': b64decode(value).decode()}
        }

        class WallpaperImageFile(BinaryFile):
            uri = '{WALLPAPER_URL}'
            storage_handler = IMAGE_STORAGE_HANDLER

            @action('postprocessor')
            def append_to_tracking_list(self, **kwargs):
                filename = os.path.basename(self.get_inherited_variable('WALLPAPER_URL'))
                self.get_inherited_variable('tracked_wallpapers').append(filename)

        sub_instruments = [WallpaperImageFile]

    sub_instruments = [WallpaperImageLink]


if __name__ == "__main__":
    WallbaseScraper().begin()
