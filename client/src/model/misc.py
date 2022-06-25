from collections import namedtuple

GemList = namedtuple('GemList', ["wanted", "offered"])
SearchResult = namedtuple('SearchResult', ["peername", "ip", "port", "key", "gems"])