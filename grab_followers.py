#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
from config import (api, logger, BREAK_AT, TARGET,
                    get_followers, save_followers)

# intro
target = api.get_user(TARGET)
logger.info("{} has {} followers".format(TARGET, target.followers_count))

# store existing list of actual followers
followers = get_followers()
existing_fids = [f['fid'] for f in followers]

# retrieve new list of followers ids
followers_ids = api.followers_ids(TARGET)
new_followers_ids = [fid for fid in followers_ids if fid not in existing_fids]

# save updated list of followers (with new ids)
for fid in new_followers_ids:
    followers.append({'fid': fid})
save_followers(followers)

logger.info("Found {} new followers IDs"
            .format(len(new_followers_ids)))

# get screen_name for each fid in followers
count = 0
for follower in followers:
    if follower.get('screen_name'):
        continue

    logger.info("Fetching screen_name for {}".format(follower['fid']))

    follower['screen_name'] = api.get_user(follower['fid']).screen_name
    count += 1

    # break after a number of requests (dev)
    if BREAK_AT and count >= BREAK_AT:
        break

save_followers(followers)

logger.info("All done.")
