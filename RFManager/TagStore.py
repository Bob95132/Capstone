import collections
import datetime

class TagStore:
    def __init__(self):
        self.size = 0
        self.tag_map = collections.defaultdict()

    def add_tags(self, ids):
        for id in ids:
            if id not in self.tag_map:
                self.tag_map[id] = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        self.size = len(self.tag_map)

    def file_dump(self):
        #write tags to file
        pass

    def get_contents_str(self):
        contents = 'TagStore: {'
        for key in self.tag_map:
            contents += '\n\t' + '%s : %s,' % (str(key), str(self.tag_map[key]))
        contents = contents[:-1]
        contents += '\n}\n'
        return contents