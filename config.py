#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import json
import os

import tweepy

CONFIG = json.load(open('config.json', 'r'))
CONSUMER_KEY = CONFIG.get('CONSUMER_KEY')
CONSUMER_SECRET = CONFIG.get('CONSUMER_SECRET')
ACCESS_TOKEN = CONFIG.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = CONFIG.get('ACCESS_TOKEN_SECRET')
TARGET = CONFIG.get('TARGET')
BREAK_AT = CONFIG.get('BREAK_AT')
PAUSE_DELAY = CONFIG.get('PAUSE_DELAY')

followers_fname = '{}_followers.json'.format(TARGET)
messages_fname = '{}_messages.json'.format(TARGET)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_followers():
    if os.path.isfile(followers_fname):
        return json.load(open(followers_fname, 'r'))
    return []


def get_messages():
    if os.path.isfile(messages_fname):
        return json.load(open(messages_fname, 'r'))
    return []


def save_followers(followers):
    with open(followers_fname, 'w') as f:
        json.dump(followers, f)
