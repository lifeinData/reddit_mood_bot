import authentication_scripts.bot_login as bot_login

def main():
    reddit = bot_login.authenticate()


if __name__ == '__main__':
    main()