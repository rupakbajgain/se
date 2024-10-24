stoppers = ' []()\n/:'#what to stop on

class WordIter:
    def __init__(self,text):
        self.text = text
        self.pos = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        word = ''
        startpos = None
        while True:
            if self.pos >= len(self.text):
                raise StopIteration
            c=self.text[self.pos]
            self.pos += 1
            if c in stoppers:
                if len(word):
                    return (startpos, word)
            else:
                if not startpos:
                    startpos=self.pos-1
                word+=c
    
def count_words(s,wl):
    d = {}
    for i in wl:
        d[i]=[]
    for c,w in WordIter(s):
        x = w.lower()
        if x in wl:
            d[x].append(c)
    return d