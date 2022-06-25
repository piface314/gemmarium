from kivy.factory import Factory
from kivy.lang import Builder

Builder.load_file('src/view/component/popup.kv')


def Loading():
    return Factory.Loading()


def Warning(msg: str, title: str = 'Erro'):
    warning = Factory.Warning()
    warning.text = msg
    warning.title = title
    return warning
