import praw

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit(client_id='Wm3sc2AymZQaLg',
                         client_secret='eJkr3x-B0Va96ePlY5abhLjL7X0',
                         password='Origami321!',
                         user_agent='testscript by /u/reddit_mooder_bot',
                         username='reddit_mooder_bot')
    limits = reddit.auth.limits
    print('Authenticated as {}\n'.format(reddit.user.me()))
    print('Here are the limits for today \n' + str(limits))
    return reddit
