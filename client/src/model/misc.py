from collections import namedtuple

GemList = namedtuple('GemList', ["offered", "wanted"])
SearchResult = namedtuple('SearchResult', ["peername", "ip", "port", "key", "gems"])