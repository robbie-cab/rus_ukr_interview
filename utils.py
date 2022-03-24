import pathlib

import diskcache

RESOURCE_DIR = "data/resources/"
FIG_DIR = "figures/"

CACHE_TIME_LIMIT = 60 * 60 * 12
__here__ = pathlib.Path(__file__).parent
__cache__ = __here__ / ".." / ".cache"
CACHE = diskcache.Cache(__cache__)
