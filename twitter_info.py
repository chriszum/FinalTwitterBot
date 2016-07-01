import requests
import os
from twitter import Twitter, OAuth, TwitterHTTPError
from random import randint
from time import sleep

def get_twit_info(listurl):
    response2 = requests.get(listurl)
    assert response2.status_code == 200, 'Wrong status code'
    cool_list = response2.content
    cool_csv = list(cool_list.splitlines())
    CONSUMER_KEY = (cool_csv[0])
    print ("CONSUMER_KEY = " + CONSUMER_KEY)
    CONSUMER_SECRET = (cool_csv[1])
    print ("CONSUMER_SECRET = " + CONSUMER_SECRET)
    OAUTH_TOKEN = (cool_csv[2])
    print ("OAUTH_TOKEN = " + OAUTH_TOKEN)
    OAUTH_SECRET = (cool_csv[3])
    print ("OAUTH_SECRET = " + OAUTH_SECRET)
    TWITTER_HANDLE = (cool_csv[4])
    print ("TWITTER_HANDLE = " + TWITTER_HANDLE)
    follow = (cool_csv[5])
    how_many = int(follow)
    print ("We will follow = " + follow + ' users')
    sheeturl = (cool_csv[6])
    print ("The Url of your list = " + sheeturl + ' users')
    email = (cool_csv[7])
    print ("Email = " + email)
    response = requests.get(sheeturl)
    assert response.status_code == 200, 'Wrong status code'
    sheet_follow_list = response.content
    print sheet_follow_list
    cool_list = list(sheet_follow_list.splitlines())

    if not os.path.isfile(TWITTER_HANDLE +'.txt'):
        with open(TWITTER_HANDLE +'.txt', "w") as out_file:
            out_file.write("0")


    with open (TWITTER_HANDLE +'.txt', "r") as myfile:
        data=myfile.read()
        count = int(data) + 1


    newtxt = str(count)
    print("Grabbing number " + newtxt + " in the list")

    text_file = open(TWITTER_HANDLE +'.txt', "w")
    text_file.write(newtxt)
    text_file.close()
    cool_user = (cool_list[count])

    ALREADY_FOLLOWED_FILE = TWITTER_HANDLE + '-already-followed.csv'
    NO_MATTER_WHAT_FILE = TWITTER_HANDLE + '-keep-following.csv'


    t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))

    if not os.path.isfile(NO_MATTER_WHAT_FILE):
        keep_following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"])
        print("we will not unfollow " + str(keep_following))
        with open(NO_MATTER_WHAT_FILE, "w") as out_file:
            for val in keep_following:
                out_file.write(str(val) + "\n")
    

    print('unfollowing now')
    
    def auto_unfollow_nonfollowers(count=10):


        """
            Unfollows everyone who hasn't followed you back
        """

        following = set(t.friends.ids(screen_name=TWITTER_HANDLE)["ids"][:count])
        followers = set(t.followers.ids(screen_name=TWITTER_HANDLE)["ids"])

        # put user IDs here that you want to keep following even if they don't
        # follow you back
        do_not_stop_following = set()
        dnsf_list = []
        with open(NO_MATTER_WHAT_FILE) as in_file:
            for line in in_file:
                dnsf_list.append(int(line))

        do_not_stop_following.update(set(dnsf_list))
        users_keep_following = dnsf_list
        del dnsf_list

        return do_not_stop_following


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

    auto_unfollow_nonfollowers(how_many)
    def get_do_not_follow_list():
        """
            Returns list of users the bot has already followed.
        """

        # make sure the "already followed" file exists
        if not os.path.isfile(ALREADY_FOLLOWED_FILE):
            with open(ALREADY_FOLLOWED_FILE, "w") as out_file:
                out_file.write("")

            # read in the list of user IDs that the bot has already followed in the
            # past
        do_not_follow = set()
        dnf_list = []
        with open(ALREADY_FOLLOWED_FILE) as in_file:
            for line in in_file:
                dnf_list.append(int(line))

        do_not_follow.update(set(dnf_list))
        del dnf_list

        return do_not_follow

    def auto_follow_followers_for_user(user_screen_name, count=10):
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
    print('now we are following the users of ' + cool_user)
    auto_follow_followers_for_user(cool_user, how_many)
    import smtplib

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("zumtobelc@gmail.com", "ch12zu92")
    msg = ("Tweety Fired! Today was @%s" % cool_user)
    server.sendmail("zumtobelc@gmail.com", email, msg)
    server.quit()
    execfile('execute.py')
