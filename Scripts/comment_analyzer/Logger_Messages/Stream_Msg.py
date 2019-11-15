class StreamMsg:
    # Logger Messages specific to comment stream stats
    def __init__(self):
        self.subred_dict = {}

    def print_subreddit_count(self):
        print(self.subred_dict)

    def append_subred_stats(self, subred):
        if subred not in self.subred_dict.keys():
            self.subred_dict[subred] = 1
        else:
            self.subred_dict[subred] += 1
