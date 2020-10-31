# coding: utf-8
# !/usr/bin/python3
from Utils import *
from Schema import Schema

class Phraser():
    """
    Session note Phraser.
    """
    def __init__(self) -> None:
        """
        args
        """
        self.headed = False # Todo: maintain it.
        self.head = [
            Pat("Date & time: <date & time>"),
            Pat("Student: <student>"),
            Pat("Consultant: <consultant>"),
            Pat("Session note: ")
        ]
        self.phrased = False # Todo: maintain it.
        self.phrases: list(Pat) = [
            # Pat("The student came in with <item> <status>."),
            # Pat("<gender:his> <aspect> is <comment>"),
            Pat("The student came in with her <item>, discussing <topic>. <thesis> <merit> However, <setback> After some discussion, we agreed that <gender: his> needs to <discussion>. <conclusion> After the session, <afterwards>")
        ]
        self.session = {}
        self.note = []
    def add_schema(self, schema: Schema):
        self.session.update(schema.content_fixed())
        return self
    def apply_schema(self):
        if not self.headed:
            for head in self.head:
                for elt in head.attr:
                    if elt.name in self.session.keys():
                        elt.content = self.session[elt.name]
            self.headed = True
        for i in range(len(self.phrases)):
            for j in range(len(self.phrases[i].attr)):
                elt = self.phrases[i].attr[j]
                if elt.name in self.session.keys():
                    elt.content = self.session[elt.name]
        return self
    def analyze(self):
        pass
    def output(self, verbose: bool=False):
        # Todo: Only paragraph 0 is valid.
        if verbose:
            print("----------(Schema)----------")
            print(Schema.dumps(self.session))
            if self.headed:
                print("-----------(Head)-----------")
                for head in self.head:
                    print(head)
            if (len(self.phrases)):
                print("----------(Phrase)----------")
                print(self.phrases[0])
            print("------------(End)------------")
        else:
            if self.headed:
                for head in self.head:
                    print(head)
            print(self.phrases[0])
    def input(self, sentence: str):
        pass
