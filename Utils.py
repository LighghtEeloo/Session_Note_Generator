# coding: utf-8
# !/usr/bin/python3

class Elt():
    def __init__(self, name: str, auto: str=None, index: int=None, content: str=None):
        # Todo: parse auto pattern after parsing Pat
        if auto is None:
            if ti := name.find(':') != -1:
                auto = name[ti+1:]
                name = name[:ti+1]
        self.name = name
        self.auto = auto
        self.index = index
        self.content = content
        # print("::", (name, auto))
    def __repr__(self) -> str:
        return f'{self.name}{": " + self.content if self.content else ""}'

class Pat():
    """
    raw, attr || fromElt
    default: Pat("abc<xyz>")
    default: Pat("abc", [Elt("xyz")])
    fromElt: Pat(fromElt=Elt("<xyz>"))
    """
    def __init__(self, raw: str=None, attr: list=None, tag: str="<>", fromElt: Elt=None):
        if not fromElt is None and raw is None:
            raw = fromElt.name
        if attr is None:
            self.raw, self.attr = self.elementize(raw, attr, tag)
        else:
            self.raw = raw
            self.attr = attr
        self.tag = tag
    def __repr__(self) -> str:
        raw_lst = "".join(("--", self.raw, "--")).split("<>")
        for i in range(len(self.attr)-1,-1,-1):
            raw_lst.insert(i+1,f"<{self.attr[i]}>")
        return "".join(raw_lst)[2:-2]
    @staticmethod
    def search(raw: str, tag: str="<>") -> tuple:
        """
        raw: str, tag: two chars
        search("raw <string>", "<>") -> ("raw <>", "string")
        search("raw <string> is <bad>", "<>") -> ("raw <> is <bad>", "string")
        search("raw <> is <bad>", "<>") -> ("raw <> is <>", "bad")
        search("raw <> is <>", "<>") -> ("raw <> is <>", None)
        """
        cur = -1
        dep = 0
        for i in range(len(raw)):
            if raw[i] == tag[0]:
                dep += 1
                if cur == -1:
                    cur = i
            elif cur != -1 and raw[i] == tag[1]:
                dep -= 1
                if dep == 0:
                    if cur != i - 1:
                        return "".join((raw[0:cur+1], raw[i:])), raw[cur+1:i]
                    else:
                        cur = -1
        return raw, None
    @staticmethod
    def search_iter(raw: str, tag: str="<>") -> tuple:
        """
        search_iter("raw <string> is <bad>", "<>") -> ("raw <> is <>", ["string", "bad"])
        search("raw <> is <>", "<>") -> ("raw <> is <>", [])
        """
        lst = []
        while True:
            raw, res = Pat.search(raw, tag)
            if res is None:
                break
            else:
                lst.append(res)
        return raw, lst
    @staticmethod
    def elementize(raw: str, elements: list=None, tag: str="<>"):
        raw, lst = Pat.search_iter(raw, tag)
        # print(f'>> {raw}, {list(map(Elt,lst))}')
        return raw, list(map(Elt,lst))
