# coding: utf-8
# !/usr/bin/python3

class Elt():
    def __init__(self, name: str=None, index: int=None, content: str=None):
        self.name = name
        self.index = index
        self.content = content
    def __repr__(self) -> str:
        return f'{self.name}{": " + self.content if self.content else ""}'

def search(raw: str, tag: str="<>") -> tuple:
    """
    raw: str, tag: two chars
    search("raw <string>", "<>") -> ("raw <>", "string")
    search("raw <string> is <bad>", "<>") -> ("raw <> is <bad>", "string")
    search("raw <> is <bad>", "<>") -> ("raw <> is <>", "bad")
    search("raw <> is <>", "<>") -> ("raw <> is <>", None)
    """
    cur = -1
    for i in range(len(raw)):
        if cur == -1 and raw[i] == tag[0]:
            cur = i
        elif cur != -1 and raw[i] == tag[1]:
            if cur != i - 1:
                return "".join((raw[0:cur+1], raw[i:])), raw[cur+1:i]
            else:
                cur = -1
    return raw, None

def search_iter(raw: str, tag: str="<>") -> tuple:
    """
    search_iter("raw <string> is <bad>", "<>") -> ("raw <> is <>", ["string", "bad"])
    search("raw <> is <>", "<>") -> ("raw <> is <>", [])
    """
    lst = []
    while True:
        raw, res = search(raw, tag)
        if res is None:
            break
        else:
            lst.append(res)
    return raw, lst

def elementize(raw: str, elements: list=None, tag: str="<>"):
    raw, lst = search_iter(raw, tag)
    return raw, list(map(Elt,lst))

class Pat():
    def __init__(self, raw: str, attr: list=None, tag: str="<>"):
        if attr is None:
            self.raw, self.attr = elementize(raw, attr, tag)
        else:
            self.raw = raw
            self.attr = attr
        self.tag = tag
    def __repr__(self) -> str:
        raw_lst = "".join(("--", self.raw, "--")).split("<>")
        for i in range(len(self.attr)-1,-1,-1):
            raw_lst.insert(i+1,f"<{self.attr[i]}>")
        return "".join(raw_lst)[2:-2]


class Session():
    """
    Contains session note prototype.
    """
    def __init__(self) -> None:
        """
        args
        """
        self.note = ["Session note:", "\n"]
        self.statusTree = ["opening", "main", "conclusion"]
        self.status = 0
        self.phrases = [
            Pat("The student came in with <item> <status>."),
        ]
    def output(self):
        pass
    def input(self, sentence: str):
        pass

if __name__ == "__main__":
    session = Session()
    # print(Pat("string is <bad>, really, <comment>."))
