import operator
# from datetime import datetime

# from scxrapper.instruments.pages.cached.handlers import FilesystemPassthroughHandler
# 
# COLLECTION_PATH = '/Library/Screen Savers/Default Collections/Wallbase/'
# IMAGE_STORAGE_HANDLER = FilesystemPassthroughHandler(COLLECTION_PATH)

RESOLUTION_OPERATORS = {
    'At least': 'gteq',
    'Exactly': 'eqeq',
}

def _round_format(floats):
    return map(lambda f: '{0:.2f}'.format(f), floats)

def _divide_ratios(ratios):
    return map(lambda s: operator.truediv(*map(int, s.split(':'))), ratios)

def join_aspect_ratios(*ratios):
    """
    Splits a ratio like "4:3" into [4, 3], performs division to 1.33, and then joins all ratios
    together with a "+" sign.
    
    Example input:  ('4:3', '16:10')
    Example output: '1.33+1.60'

    """
    return '+'.join(_round_format(_divide_ratios(ratios)))


def set_categories(general=True, anime=True, high_resolution=True):
    """ general=WG, anime=W, high_resolution=HR """
    bits = []
    if general:
        bits.append(2)
    if anime:
        bits.append(1)
    if high_resolution:
        bits.append(3)
    return ''.join(map(str, bits))
