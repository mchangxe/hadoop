from mrjob.job import MRJob
from mrjob.step import MRStep


class TwitterFollowers(MRJob):
    '''
        Input: List of follower relationships in the format "user_1 user_2",
            indicating that user_1 follows user_2 (input type is string)
        Output: A list of user pairs <user_a, user_b> such that:
                - User_a follows user_b
                - User_b follows user_a
                - User_a has at least 10 followers
                - User_b has at least 10 followers
            Output key/value tuple format:
                Key: Mutual follower pair member with lesser id (int)
                Value: Mutual follower pair member with greater id (int)
    '''
    
    def mapper_count_followers(self, _, val):
        lines = val.splitlines()
        for line in lines:
            key, value = line.split()
            yield(value, key)
        
    def reducer_only_ten(self, key, vals):
        count = 0
        values = [];

        for val in vals:
            count += 1
            values.append(val)

        if count >= 10: 
            for val2 in values:
                if int(key) < int(val2):
                    yield(key, val2)
                else:
                    yield(val2, key)
            

    def mapper_count_friendship(self, key, val):
        yield ((key,val), 1) 

    def reducer_final(self, key, vals):
        count = 0
        for val in vals:
            count += 1

        if count == 2:
            yield int(key[0]), int(key[1])

    def steps(self):
        return [
            MRStep(mapper = self.mapper_count_followers, 
                reducer = self.reducer_only_ten),
            MRStep(mapper = self.mapper_count_friendship,
                reducer = self.reducer_final)
        ]

if __name__ == '__main__':
    TwitterFollowers.SORT_VALUES = True
    TwitterFollowers.run()