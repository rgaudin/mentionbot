#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import time
import random

from config import (api, logger, PAUSE_DELAY, tweepy,
                    get_followers, save_followers, get_messages)


def tweet_and_wait(message, media=None):
    logger.info(message)
    if media:
        api.update_with_media(media, message)
    else:
        api.update_status(message)
    time.sleep(PAUSE_DELAY)

followers = get_followers()
messages = get_messages()
assert len(messages) > 0
random.shuffle(followers)

for follower in followers:
    # skip completed ones
    if follower.get('handled', False):
        continue

    # mark as complete
    follower['handled'] = True
    save_followers(followers)

    message = random.choice(messages)
    try:
        tweet_and_wait(message.get("text")
                       .format(screen_name=follower['screen_name']),
                       media=message.get("media"))
    except tweepy.error.TweepError as e:
        logger.exception(e)

logger.info("All done")
