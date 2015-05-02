import praw
import time

r = praw.Reddit(user_agent = '/u/TheCard\'s moderator for /r/MaddenUltimateTeam that removes posts meeting certain criteria')
r.login()

alreadyModerated = []
#TODO: ADD MORE HERE
pullWords = ['snipe', 'pull', 'offer', '99', 'got', 'omg', 'quicksell', 'trio', 'badge', '...'] 
wasBriefed = []
wasBriefedPull = []

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
                    r.set_flair(subreddit, submission, 'scammeralert', 'scammeralert')
                elif submission.domain == 'imgur.com':
                    msg = submission.short_link
                    r.send_message('/r/CardsCreations', 'Possible Pull', msg)
                    time.sleep(10)
                elif 'mrmutcoin' in submission.title or 'mrmutcoin' in submission.domain:
                    submission.remove()
            alreadyModerated.append(submission.id)
    time.sleep(10)