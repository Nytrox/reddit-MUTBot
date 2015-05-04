import praw
import time
import random

r = praw.Reddit(user_agent = '/u/TheCard\'s and /u/NeonNytrox\'s moderator for /r/MaddenUltimateTeam that removes posts meeting certain criteria')
r.login('MUTMod', "901n324oiDDa/;'")

alreadyModerated = []
#TODO: ADD MORE HERE
pullWords = ['snipe', 'pull', 'offer', '99', 'got', 'omg', 'quicksell', 'trio', 'badge', '...'] 
wasBriefed = []
wasBriefedPull = []
    
def GiveawayWinner(GiveawayURL):
    random.seed(time.clock())
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
        Winner = r.get_redditor(l[WinnerNum])
        #To find account age, initialize a user object and call the variable 'created'.
        #Variable is returned in seconds since Epoch, so we need to have the six months in Seconds since Epoch too
        sixMonths = 15552000
        if Winner.created - sixMonths >= 0:
            WinnerFound = True
        
        return Winner
    
def checkInbox():
    #PlaceHolder so we don't get errors for an empty method
    return True
    
while True:
    subreddit = r.get_subreddit('mutmod')
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
                    r.send_message(submission.author, 'Giveaway ' + submission.short_link, 'Do you want us to handle your giveaway for you? Reply with a "y" for yes. Otherwise, no need to reply. To learn more, read [here](www.reddit.com/r/MUTMod/wiki.giveaway)')
                    #GiveawayWinner returns the winner, so we just call the method and put that as the recipient
                    r.send_message(GiveawayWinner(submission.url), 'Congrats', 'You won the giveaway')
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
