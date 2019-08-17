run_scraper = True
current_epoch = None
time_list = []
first_run = True
n = 0

while run_scraper:
    payload = {'after': get_dynamic_seconds(current_epoch), 'size':'500', 'subreddit':'AskReddit', 'sort':'desc'}

    if first_run == True:
        current_epoch = int(time.time())
    
    resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params = payload)
    # might loss some comments based on speed of processing here (between getting resp and the next int(time.time()))
    
    print ('# of comments: {} ||| Elasped time: {}'.format(len(resp.json()['data']), int(time.time()) - current_epoch))
    
    if len(resp.json()['data']) > 1 and first_run == False:
        print ('rest current time counter')
        current_epoch = int(time.time())
        
        
    for d in resp.json()['data']:
        print ('comment time {} in {}'.format(time.strftime('%H:%M:%S', time.localtime(d['created_utc'])), d['subreddit']))
#         print ('seconds since last comment {}'.format(int(curent_epoch - d['created_utc'])), time.strftime('%H:%M:%S:%f', time.localtime(d['created_utc'])))
        time_list.append (d['id'])
        n += 1
    
    if n > 1:
        first_run = False
    elif n > 10000:
        run_scraper = False