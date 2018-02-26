from mrjob.job import MRJob


class TwitterActiveUsers(MRJob):
    '''
        Input: List of lines containing tab-separated tweets with following format:
            POST_DATETIME <tab> TWITTER_USER_URL <tab> TWEET_TEXT

        Output: A generated list of key/value tuples:
            Key: Day in `YYYY-MM-DD` format
            Value: Twitter user handle of the user with the most tweets on this day
                (including '@' prefix)
    '''

    def mapper(self, key, val):
        for line in val.splitlines():
            if(line):
                tabsep = line.split("\t")
                if(tabsep):
                    yield((tabsep[0].split())[0], "@"+tabsep[1].replace('http://twitter.com/',''))

    def reducer(self, key, vals):

        mp = {}

        for val in vals:
            if val in mp:
                mp[val] += 1
            else:
                mp[val] = 1

        mp = sorted(mp.items(), key=lambda x: (-x[1],x[0]))
        # print(mp)
        yield(key, mp[0][0])



if __name__ == '__main__':
    TwitterActiveUsers.SORT_VALUES = True
    TwitterActiveUsers.run()