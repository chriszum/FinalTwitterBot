import smtplib
import os

def send_email(email, cool_user):

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("zumtobelc@gmail.com", "ch12zu92")
	msg = ("Tweety Fired! Today was @%s" % cool_user)
	server.sendmail("zumtobelc@gmail.com", email, msg)
	server.quit()

def count_users(TWITTER_HANDLE):

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
