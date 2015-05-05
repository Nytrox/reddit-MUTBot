import praw
import time
import random

r = praw.Reddit(user_agent = '/u/TheCard\'s and /u/NeonNytrox\'s moderator for /r/MaddenUltimateTeam that removes posts meeting certain criteria')
r.login()

alreadyModerated = []
#TODO: ADD MORE HERE
pullWords = ['snipe', 'pull', 'offer', '99', 'got', 'omg', 'quicksell', 'trio', 'badge', '...', 'bang', 'boom'] 
wasBriefed = []
wasBriefedPull = []
giveawayTimes, giveawayURLs = [], []
    
def GiveawayWinner(GiveawayURL):
    random.seed(time.time())
    l, WinnerFound, numbOfComments, prevAuthors = [], False, 0, []
    submission = r.get_submission(url=GiveawayURL, submission_id=None, comment_limit=None)
    comments = submission.comments #first parameter in get_comments is for the subreddit. Instead we want comments in the submission
    for comment in comments:
        #There's probably an easier way to do this, like only finding the roots of the forest
        #Like maybe I can use praw.helpers.flatten_tree(tree, nested_attr=u'replies', depth_first=False)
        if comment.is_root:
            #Duplicate Check
            if comment.author not in prevAuthors:
                prevAuthors.append(comment.author)
                l.append(comment.author) 
                numbOfComments += 1 #God dammnit Python, please add a ++ operator
                time.sleep(10) #The preceeding for loop is extremely intensive as far as API calls go, so we let the bot sleep so we don't get disconnected from the server
    while WinnerFound == False:
        WinnerNum = random.randint(0, numbOfComments-1)
        #Gets the author of the winning comment
        Winner = l[WinnerNum]
        #To find account age, initialize a user object and call the variable 'created'.
        #Variable is returned in seconds since Epoch, so we need to have the six months in Seconds since Epoch too
        sixMonths = 15552000
        if Winner.created - sixMonths >= 0:
            WinnerFound = True
        
        r.send_message(Winner, 'Congrats', 'You\'ve won the giveaway! Please contact the giveaways author to receive your prize; we\'ll let them know you won.')
        time.sleep(2) #Ugh so many disconnects
        msg = Winner + 'has won your giveaway. Please message them and arrange the card exchange. They have been notified as well.'
        r.send_message(submission.author, 'Your giveaway winner', msg)
    
def checkInbox():
    #Variable to store PMs in
    pms = None
    #Get all unread messages
    pms = r.get_unread(limit = none)
    
    if pms is not None:
        for pm in pms:
            #Check for giveaway replies
            if 'Giveaway' in pm.subject:
                giveawayURL = pm.[9:]
                #see if they're saying they want mutmod to handle their giveaway
                if pm.body.lower() == 'y' or pm.body.lower() == 'yes':
                    pm.reply('Great! Please now reply the amount of hours you want the giveaway to end in. Please reply with the digit only, and keep the rest of the PM empty. Thank you.')
                #See if the reply is a digit, i.e. a time
                if pm.body.isdigit():
                    #Set a time (in seconds since epoch) for giveaway bot to run (3600 seconds == 1 hour)
                    giveawayTimes.append(int(pm.body) * 3600 + time.time())
                    giveawayURLs.append(giveawayURL)
            else:
                #Forward every message to the modmail of the subreddit
                r.send_message('/r/MaddenUltimateTeam', 'Message', pm.body)
            time.sleep(2)
            pm.mark_as_read()
    
while True:
    subreddit = r.get_subreddit('MaddenUltimateTeam')
    for submission in subreddit.get_new(limit = 10):
        if submission.id not in alreadyModerated:
            #Welcome new members
            if submission.author not in wasBriefed:
                #TODO: ADD WELCOME MESSAGE
                msg = "Welcome to /r/MaddenUltimateTeam! This is your first post in the sub. There are some cool features that we'd like to let you know about."
                r.send_message(submission.author, 'Welome to /r/MaddenUltimateTeam', msg)
            
            if submission.is_self:
                #Remove mrmutcoin
                if 'mrmutcoin' in submission.title.lower() or 'mrmutcoin' in submission.selftext.lower():
                    selfText = submission.selftext.lower()
                    submission.remove()
                #All of the following below in self posts, not link posts
                #Giveaway
                elif "giveaway" in submission.title.lower() and "thanks" not in submission.title.lower():
                    r.set_flair(subreddit, submission, 'giveaway', 'giveaway')
                    r.send_message(submission.author, 'Giveaway ' + submission.url, 'Do you want us to handle your giveaway for you? Reply with a "y" for yes. Otherwise, no need to reply. To learn more, read [here](www.reddit.com/r/MUTMod/wiki.giveaway)')
                #Review
                elif "review" in submission.title.lower() and "?" not in submission.title.lower():
                    r.set_flair(subreddit, submission, 'review', 'review')
                #Stream
                elif submission.domain == 'twitch.tv':
                    r.set_flair(subreddit, submission, 'stream', 'stream')
                #Scammer
                elif "scammer" in submission.title.lower():
                    r.set_flair(subreddit, submission, 'SCAMMER ALERT', 'scammeralert')
                #Remove mrmutcoin
            else:
                #Pull
                isPull = any(string in submission.title.lower() for string in pullWords)
                if submission.domain == 'imgur.com' and isPull:
                    r.set_flair(subreddit, submission, 'pull', 'pull')
                    #'Brief' someone about the find pull function of this bot if they have not already made a post that has been flaired
                    if submission.author not in wasBriefedPull:
                        msg = 'This is the only time you\'ll receive this message. Your post has been flaired as a pull due to it meeting certain criteria. Please [message the mods if this is a mistake](https://www.reddit.com/message/compose?to=%2Fr%2FMaddenUltimateTeam) From now on, please make sure your posts to imgur.com are not flaired incorrectly. \n\n I am a bot, please message [my creator](/u/TheCard) if you have a problem.'
                        subject = 'Pull'
                        user = submission.author
                        r.send_message(user, subject, msg)
                        wasBriefedPull.append(submission.author)
                #Possible pull
                elif submission.domain == 'imgur.com':
                    r.send_message('/r/MaddenUltimateTeam', 'Possible Pull', submission.short_link)
                #any operator was used only to test for a list of words. In and not in operators should suffice for simple words.
                elif 'mrmutcoin' in submission.title.lower() or 'mrmutcoin' in submission.domain:
                    submission.remove()
            alreadyModerated.append(submission.id)
    checkInbox()        
    #Sleep so we abide by the Reddit API rules
    time.sleep(15)
    #Check times for scheduled giveaways
    #20 second range on each side to reduce error
    iterated = -1
    for giveawayTime in giveawayTimes:
    iterated += 1
        if time.time() - 25 <= giveawayTime <= time.time() + 25:
            GiveawayWinner(giveawayURLs[iterated])
            #Remove giveaway URL and times so they are not repeated
            giveawayURLs.pop(0)
            giveawayTimes.pop(0)
