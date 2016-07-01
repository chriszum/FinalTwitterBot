# -*- coding: utf-8 -*-

"""
Copyright 2014 Randal S. Olson

This file is part of the Twitter Follow Bot library.

The Twitter Follow Bot library is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option) any
later version.

The Twitter Follow Bot library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with the Twitter
Follow Bot library. If not, see http://www.gnu.org/licenses/.

Code only slightly modified by Programming for Marketers to allow for separate variable
storage.
"""

from twitter import Twitter, OAuth, TwitterHTTPError
import os
from random import randint
from time import sleep


# put the full path and file name of the file you want to store your "already followed"




def auto_follow_followers_for_user(user_screen_name, count=100):
    """
        Follows the followers of a user
    """
    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
    followers_for_user = set(t.followers.ids(screen_name=user_screen_name)["ids"][:count]);
    do_not_follow = get_do_not_follow_list()

    for user_id in followers_for_user:
        try:
            sleep(randint(0,5))
            if (user_id not in following and
                user_id not in do_not_follow):

                t.friendships.create(user_id=user_id, follow=False)
                print(TWITTER_HANDLE + "followed %s" % user_id)

        except TwitterHTTPError as e:
            print("error: %s" % (str(e)))

def auto_unfollow_nonfollowers(count=30):
    from twitter_info import *

    ALREADY_FOLLOWED_FILE = TWITTER_HANDLE + '-already-followed.csv'


    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))
    """
        Unfollows everyone who hasn't followed you back
    """

    following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"][:count])
    followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

    # put user IDs here that you want to keep following even if they don't
    # follow you back
    users_keep_following = set([])

    not_following_back = following - followers

    # make sure the "already followed" file exists
    if not os.path.isfile(ALREADY_FOLLOWED_FILE):
        with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
            out_file.write("")

    # update the "already followed" file with users who didn't follow back
    already_followed = set(not_following_back)
    af_list = []
    with open(ALREADY_FOLLOWED_FILE) as in_file:
        for line in in_file:
            af_list.append(int(line))

    already_followed.update(set(af_list))
    del af_list

    with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
        for val in already_followed:
            out_file.write(str(val) + "\n")

    for user_id in not_following_back:
        sleep(randint(0,5))
        if user_id not in users_keep_following:
            t.friendships.destroy(user_id=user_id)
            print(TWITTER_HANDLE + "unfollowed %d" % (user_id))

