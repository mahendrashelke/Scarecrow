from os import curdir

WORKDIR = curdir

COGS = WORKDIR + '/cogs/'

CONFIG = WORKDIR + '/conf/'
SCARECROW_CONFIG = CONFIG + 'scarecrow.json'
TWITTER_CONFIG = CONFIG + 'twitter.json'

DATA = WORKDIR + '/data/'
INSULTS = DATA + 'insults.txt'
WEEBNAMES = DATA + 'weeb_names.txt'

LOGS = WORKDIR + '/logs/'
SCARECROW_LOG = LOGS + 'scarecrow.log'
TWITTER_SUBPROCESS_LOG = LOGS + 'twitter-sub-process-{pid}.log'