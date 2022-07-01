from ctrl.search import SearchCtrl
from ctrl.trade import TradeCtrl
from kivy.app import App
from kivy.clock import mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from model.misc import GemList, SearchResult
from view.component.popup import Loading, Warning
import threading
import traceback

Builder.load_file('src/view/screen/search.kv')

class SearchPopup(Popup):

    data = ObjectProperty(SearchResult("", "", "", 0, b'', GemList([], []), False))
    start_trade = ObjectProperty(None)


class SearchScreen(Screen):

    results = ObjectProperty([])
    query_type = BooleanProperty(True)
    check_icon = ObjectProperty(None)
    search_icon = ObjectProperty(None)
    gsearch_icon = ObjectProperty(None)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
        self.ctrl: SearchCtrl = app.search_ctrl
        self.check_icon = app.get_texture('buttons-accept')
        self.search_icon = app.get_texture('buttons-search')
        self.gsearch_icon = app.get_texture('buttons-gsearch')

    @mainthread
    def on_results(self, *args):
        res = self.ids['results']
        res.labels = [self.format_label(r) for r in self.results]

    def on_query_type(self, *args):
        res = self.ids['results']
        res.labels = [self.format_label(r) for r in self.results]
    
    def format_label(self, res: SearchResult):
        color = 'ffcc00' if res.matches else 'cccccc'
        return f'@{res.peername}\n[size=12][color={color}]{res.gems[int(self.query_type)]}[/color][/size]'

    def search(self, query):
        loading = Loading()
        loading.open()
        worker = threading.Thread(target=self.resolve_search, args=(loading, query, True))
        worker.start()

    def global_search(self):
        popup = Warning("Funcionalidade de busca global ainda não foi implementada! :(")
        popup.open()

    def resolve_search(self, loading, query, is_local):
        try:
            self.results = self.ctrl.search(query, self.query_type, is_local=is_local)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            self.show_warning("Erro desconhecido.")
        finally:
            loading.dismiss()
    
    @mainthread
    def show_warning(self, msg):
        popup = Warning(msg)
        popup.open()
    
    def goto_result(self, row):
        sr = self.results[row.index]
        popup = SearchPopup(
            data=sr,
            start_trade=self.start_trade
        )
        popup.open()
    
    def start_trade(self, sr: SearchResult):
        app = App.get_running_app()
        ctrl: TradeCtrl = app.trade_ctrl
        loading = Loading()
        def cb():
            try:
                trade = ctrl.start_trade(sr)
                app.current_peer = trade.peerid
                self.goto_trade()
            except:
                self.show_warning("Erro desconhecido.")
            finally:
                loading.dismiss()
        worker = threading.Thread(target=cb)
        loading.open()
        worker.start()
        
    @mainthread
    def goto_trade(self):
        self.manager.current = 'trade'
        