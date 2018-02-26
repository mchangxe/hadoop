from mrjob.job import MRJob
import re, string



class TwitterAtMentions(MRJob):
    '''
        Input: List of lines containing tab-separated tweets with following format:
            POST_DATETIME <tab> TWITTER_USER_URL <tab> TWEET_TEXT

        Output: A generated list of key/value tuples:
            Key: Twitter user handle (including '@' prefix)
            Value: Number of @-mentions received
    '''
    def mapper(self, key, val):

        for line in val.splitlines():
            if (line):
                tabsep = line.split("\t")
                tweet = tabsep[2]
                if(tweet):
                    output = re.findall(r'(@\w{3,15})\b', tweet)
                    # output = re.findall("@([a-zA-Z0-9_]{3,15})", tweet)
                    for mentions in set(output):
                        yield(mentions, 1)

    def reducer(self, key, vals):
        count = 0

        for _ in vals:
            count += 1

        yield(key, count)


if __name__ == '__main__':
    TwitterAtMentions.run()