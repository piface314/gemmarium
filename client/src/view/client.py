from ctrl.collection import CollectionCtrl
from ctrl.profile import ProfileCtrl
from ctrl.search import SearchCtrl
from ctrl.trade import TradeCtrl, TradeEvent
from kivy.app import App
from kivy.clock import mainthread
from kivy.core.image import Image, TextureRegion
from kivy.uix.screenmanager import ScreenManager, CardTransition, FallOutTransition
from kivy.factory import Factory
from view.component.holder import GemHolder
from view.screen import (
    CollectionScreen,
    MenuScreen,
    OfferedScreen,
    RequestScreen,
    SearchScreen,
    SignupScreen,
    TradeListScreen,
    TradeScreen,
    WantedScreen
)


class ClientApp(App):

    def __init__(self,
                 collection_ctrl: CollectionCtrl,
                 profile_ctrl: ProfileCtrl,
                 search_ctrl: SearchCtrl,
                 trade_ctrl: TradeCtrl,
                 **kwargs):
        super(ClientApp, self).__init__(**kwargs)
        self.screen_history = []
        self.textures = {}
        self.current_peer = None
        self.collection_ctrl = collection_ctrl
        self.profile_ctrl = profile_ctrl
        self.search_ctrl = search_ctrl
        self.trade_ctrl = trade_ctrl

    def build(self):
        self.icon = 'res/icon.png'
        self.title = 'Gemmarium'

        sm = ScreenManager(transition=CardTransition())
        if not self.profile_ctrl.is_logged_in():
            sm.add_widget(SignupScreen(name='signup'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(CollectionScreen(name='collection'))
        sm.add_widget(OfferedScreen(name='offered'))
        sm.add_widget(WantedScreen(name='wanted'))
        sm.add_widget(RequestScreen(name='request'))
        sm.add_widget(SearchScreen(name='search'))
        sm.add_widget(TradeListScreen(name='trade_list'))
        sm.add_widget(TradeScreen(name='trade'))
        return sm
    
    def on_start(self):
        self.trade_ctrl.bind(TradeEvent.GEMS, self.show_gems)
        self.load_textures('base')
        self.load_textures('buttons', [
            ('search', 0, 32, 16, 16),
            ('gsearch', 16, 32, 16, 16),
            ('back', 0, 16, 16, 16),
            ('edit_offered', 16, 16, 16, 16),
            ('edit_wanted', 32, 16, 16, 16),
            ('trade', 48, 16, 16, 16),
            ('reject', 0, 0, 16, 16),
            ('accept', 16, 0, 16, 16),
            ('fusion', 32, 0, 16, 16),
            ('add', 48, 0, 16, 16),
        ])
    
    @mainthread
    def show_gems(self, sender, gems):
        if not gems:
            return
        popups = []
        for gem in gems:
            popup = Factory.GemShow()
            popup.title = "Nova gema"
            popup.text = f'@{sender} te enviou {gem.name}!'
            layout = popup.ids['layout']
            layout.add_widget(GemHolder.from_gem(gem), 1)
            popups.append(popup)
        for i in range(1, len(popups)):
            popups[i-1].bind(on_dismiss=lambda _, i=i: popups[i].open())
        popups[0].open()
    
    def load_textures(self, key, rects=None):
        fp = f'res/{key}.png'
        img = Image(fp)
        tx = img.texture
        tx.mag_filter = 'nearest'
        if rects:
            for label, x, y, w, h in rects:
                reg = TextureRegion(x, y, w, h, tx)
                self.textures[f'{key}-{label}'] = reg
        else:
            self.textures[key] = tx
    
    def get_texture(self, key):
        return self.textures.get(key, None)
    
    def go_back(self, *args):
        if self.screen_history:
            self.screen_history.pop()
            sc = self.screen_history.pop()
            t = self.root.transition
            self.root.transition = FallOutTransition()
            self.root.current = sc
            self.root.transition = t
    
    def back_to_menu(self, *args):
        self.screen_history = []
        t = self.root.transition
        self.root.transition = FallOutTransition()
        self.root.current = 'menu'
        self.root.transition = t
    
    def get_back_button(self):
        return (self.go_back, self.get_texture('buttons-back'))