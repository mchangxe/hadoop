from mrjob.job import MRJob


class WikipediaLinks(MRJob):
    '''
        Input: List of lines, each containing a user session.
            - Articles are separated by ';' characters
            - Given a session 'page_a;page_b':
                this indicates there is a link from the article page_a to page_b
            - A '<' character indicates that a user has clicked 'back' on their
                browser and has returned to the previous page they were on
        Output: The number of unique inbound links to each article
            Key: Article name (str)
            Value: Number of unique inbound links (int)
    '''

    def mapper(self, key, val):
        stack = []
        lines = val.splitlines()
        for line in lines:
            words = line.split(";")
            for index, word in enumerate(words):
                if index != 0 and word != "<":
                    dest = word
                    src = stack[-1]
                    yield(dest, src)
                    stack.append(dest)
                elif index == 0:
                    src = word
                    stack.append(src)
                    
                else:
                    stack.pop()


    def reducer(self, key, vals):
        prev, count = None, 0

        for v in vals:
            if v != prev:
                count += 1
            prev =v

        yield (key, count)


if __name__ == '__main__':
    WikipediaLinks.SORT_VALUES = True
    WikipediaLinks.run()