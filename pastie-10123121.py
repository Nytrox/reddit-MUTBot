import praw
import time

r = praw.Reddit(user_agent = '/u/TheCard\'s moderator for /r/MaddenUltimateTeam that removes posts meeting certain criteria')
r.login()

alreadyModerated = []
#TODO: ADD MORE HERE
pullWords = ['snipe', 'pull', 'offer', '99', 'got', 'omg', 'quicksell', 'trio', 'badge', '...'] 
wasBriefed = []
wasBriefedPull = []

def Giveaway(players, system):
    assert type(players) is StringType, "players is not an String: %r" % players
    assert type(system) is StringType, "system is not an String: %r" % system
    #Not sure if this works. I hope it's SubmitMixin.
    r.SubmitMixin.submit(r.get_subreddit('MaddenUltimateTeam'), system + " Giveaway!",
        text= "We are giving away " + players ". The system is " + system + "\n\n. Please comment once. Double submissions will be ignored completely. Also, your account must be older than 6 months"
        , save = True)
    r.set_flair(subreddit, submission, 'giveaway', 'giveaway')
    #Need to somehow save the URL of the submission. I saved the submission, but I need to re-access the submission
    URL = r.get_submission() #YOLO HOPE THIS WORKS
    return URL
    
def GiveawayWinner(GiveawayURL):
    l, WinnerFound = [], True
    submission = r.get_submission(url=GiveawayURL, submission_id=None, comment_limit=None)
    comments = submission.get_comments(‘all’) #get_all_comments apparently will be removed
    #How the hell do I get the number of comments? I wish I could test this out...
    for comment in comments:
        #There's probably an easier way to do this, like only finding the roots of the forest
        #Like maybe I can use praw.helpers.flatten_tree(tree, nested_attr=u'replies', depth_first=False)
        if comment.is_root():
            l.append(comment)
    while WinnerFound = True:
        WinnerNum = randint(0, l.size())
        #Get Comment Author/redditor. No idea how to do that
        Winner = l[WinnerNum].get_redditor() #totally fake/made up function
        #Damn, looks like we need to do this to get the redditor age http://www.reddit.com/r/learnpython/comments/2txd3t/praw_question_regarding_redditor_account_age/
        if redditor account age >= 6 months:
            WinnerFound = False
    return Winner
    
while True:
    subreddit = r.get_subreddit('MaddenUltimateTeam')
    for submission in subreddit.get_new(limit = 10):
        if submission.id not in alreadyModerated:
            if submission.author not in wasBriefed:
            #TODO: ADD WELCOME MESSAGE
            msg = 'something cool will be here' 
            r.send_message(submission.author, 'Welome to /r/MaddenUltimateTeam', msg)
            if submission.is_self:
                if 'mrmutcoin' in submission.title or 'mrmutcoin' in submission.selftext.lower():
                    selfText = submission.selftext.lower()
                    submission.remove()
            else:
                isPull = any(string in submission.title for string in pullWords)
                if submission.domain == 'imgur.com' and isPull:
                    r.set_flair(subreddit, submission, 'pull', 'pull')
                    if submission.author not in wasBriefedPull:
                        msg = 'This is the only time you\'ll receive this message. Your post has been flaired as a pull due to it meeting certain criteria. Please [message the mods if this is a mistake](https://www.reddit.com/message/compose?to=%2Fr%2FMaddenUltimateTeam) From now on, please make sure your posts to imgur.com are not flaired incorrectly. \n\n I am a bot, please message [my creator](/u/TheCard) if you have a problem.'
                        subject = 'Pull'
                        user = submission.author
                        r.send_message(user, subject, msg)
                        wasBriefedPull.append(submission.author)
                #Giveaway
                elif any("giveaway" in submission.title and "thanks" not in submission.title):
                    r.set_flair(subreddit, submission, 'giveaway', 'giveaway')
                #Review
                elif any("review" in submission.title and "?" not in submission.title):
                    r.set_flair(subreddit, submission, 'review', 'review')
                #Stream
                elif submission.domain == 'twitch.tv':
                    r.set_flair(subreddit, submission, 'stream', 'stream')
                #Scammer
                elif any("scammer" in submission.title):
                    r.set_flair(subreddit, submission, 'SCAMMER ALERT', 'scammeralert')
                elif submission.domain == 'imgur.com':
                    msg = submission.short_link
                    r.send_message('/r/CardsCreations', 'Possible Pull', msg)
                    time.sleep(10)
                elif 'mrmutcoin' in submission.title or 'mrmutcoin' in submission.domain:
                    submission.remove()
            alreadyModerated.append(submission.id)
    time.sleep(10)