#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import json

import tweepy

CONFIG = json.load(open('config.json', 'r'))
CONSUMER_KEY = CONFIG.get('CONSUMER_KEY')
CONSUMER_SECRET = CONFIG.get('CONSUMER_SECRET')
ACCESS_TOKEN = CONFIG.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = CONFIG.get('ACCESS_TOKEN_SECRET')
TARGET = CONFIG.get('TARGET')
BREAK_AT = CONFIG.get('BREAK_AT')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# followers
target = api.get_user(TARGET)
logger.info("{} has {} followers".format(TARGET, target.followers_count))

# retrieve list of followers
followers_ids = api.followers_ids(TARGET)
with open('{}_followers_ids.json'.format(TARGET), 'w') as f:
    json.dump(followers_ids, f)

logger.info("Found {} followers IDs".format(len(followers_ids)))

followers = []
c = 0
for fid in followers_ids:
    screen_name = api.get_user(fid).screen_name
    followers.append(screen_name)
    c += 1
    if BREAK_AT and c >= BREAK_AT:
        break

with open('{}_followers.json'.format(TARGET), 'w') as f:
    json.dump(followers, f)

from pprint import pprint as pp ; pp(followers)
