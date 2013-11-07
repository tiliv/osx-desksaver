import sys
from urllib.parse import quote

from scxrapper.instruments.pages.cached.handlers import FilesystemPassthroughHandler

from utils import join_aspect_ratios, set_categories, RESOLUTION_OPERATORS

# Example full urls:
# http://wallbase.cc/toplist/0/213/gteq/0x0/0/010/32/1d
# http://wallbase.cc/search/ 0/213/gteq/0x0/0/010/60/relevance/wallpapers/desc/60

def get_config():
    CONFIGURATION = {
        'toplist': {
            'name': 'Wallbase — Toplist',
            'uri': "http://wallbase.cc/toplist/0/{categories}/{resolution_operator}/{resolution}/{aspect_ratio}/{sfw}{sketchy}{nsfw}/{per_page}/{timeframe}",

            'per_page': 60,  # 20, 32, 40, 60
            'categories': set_categories(general=True, anime=False, high_resolution=True),

            # Purity settings must be present, but use 1 or 0 to enable or disable.
            'sfw': 1,
            'sketchy': 0,
            'nsfw': 0,

            # Resolution
            'resolution_operator': RESOLUTION_OPERATORS['At least'],  # 'At least' or 'Exactly'
            'resolution': '0x0',  # Use '0x0' for all
            'aspect_ratio': '0',  # join_aspect_ratios('4:3', '16:10'),

            # Popularity timeframe
            'timeframe': '1d',  # '1d', '3d', '1w', '2w', '1m', '2m', '3m', '0'
        },
        'search': {
            'name': 'Wallbase — Search',
            'uri': "http://wallbase.cc/search/{search}/{categories}/{resolution_operator}/{resolution}/{aspect_ratio}/{sfw}{sketchy}{nsfw}/{per_page}/{sort_by}/wallpapers/{sort_direction}/{offset}",

            'per_page': 60,  # 20, 32, 40, 60
            'categories': set_categories(general=True, anime=False, high_resolution=True),

            # Purity settings must be present, but use 1 or 0 to enable or disable.
            'sfw': 1,
            'sketchy': 0,
            'nsfw': 0,

            # Resolution
            'resolution_operator': RESOLUTION_OPERATORS['At least'],  # 'At least' or 'Exactly'
            'resolution': '0x0',  # Use '0x0' for all
            'aspect_ratio': '0',  # join_aspect_ratios('4:3', '16:10'),

            # Popularity timeframe
            'timeframe': '1d',  # '1d', '3d', '1w', '2w', '1m', '2m', '3m', '0'

            # Items for searches only:
            'search': 'abstract',
            'sort_by': 'views',  # 'relevance', 'date', 'views', 'favs', 'random'
            'sort_direction': 'desc',  # 'desc', 'asc'
            'offset': '0',
        }
    }

    CONFIGURATION['default'] = CONFIGURATION['toplist']

    args = sys.argv[1:]
    COLLECTION_PATH = '/Library/Screen Savers/Default Collections/{}/'.format(CONFIGURATION['default']['name'])
    if args:
        config = CONFIGURATION[args.pop(0)]
        if 'Search' in config['name'] and args:
            query = args.pop(0)
            config['search'] = quote(query)
            COLLECTION_PATH = 'wallpapers/{}/'.format(query)

        if args:
            config.update(**dict(zip(['sfw', 'sketchy', 'nsfw'], args.pop(0)+'000')))
            
            if args:
                config['sort_by'] = args.pop(0)
    else:
        config = CONFIGURATION['default']

    IMAGE_STORAGE_HANDLER = FilesystemPassthroughHandler(COLLECTION_PATH)
    return config, IMAGE_STORAGE_HANDLER
