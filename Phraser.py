# coding: utf-8
# !/usr/bin/python3
from Utils import *

class Phraser():
    """
    Session note Phraser.
    """
    def __init__(self) -> None:
        """
        args
        """
        self.note = ["Session note:", "\n"]
        self.statusTree = ["opening", "main", "conclusion"]
        self.status = 0
        self.phrases = [
            # Pat("The student came in with <item> <status>."),
            # Pat("<gender:his> <aspect> is <comment>"),
            Pat("The student came in with her <item>, discussing <topic>. <thesis> <merit> However, <setback> After some discussion, we agreed that <gender: his> needs to <discussion>. <conclusion> After the session, <afterwards>")
        ]
        self.waitingTree = []
    def analyze(self):
        pass
    def output(self):
        if (len(self.phrases)):
            print(self.phrases[0])
        else:
            print("----(End)----")
    def input(self, sentence: str):
        pass
