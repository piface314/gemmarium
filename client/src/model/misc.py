from collections import namedtuple

GemList = namedtuple('GemList', ["wanted", "offered"])
SearchResult = namedtuple('SearchResult', ["id", "peername", "ip", "port", "key", "gems", "matches"])
