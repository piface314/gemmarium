from ctrl.profile import ProfileCtrl
from kivy.app import App
from kivy.core.image import Image, TextureRegion
from kivy.uix.screenmanager import ScreenManager, CardTransition, FallOutTransition
from view.screen import (
    SignupScreen,
    MenuScreen,
    RequestScreen,
    TradeListScreen,
    CollectionScreen,
    SearchScreen
)


class ClientApp(App):

    def __init__(self,
                 collection_ctrl,
                 profile_ctrl: ProfileCtrl,
                 search_ctrl,
                 trade_ctrl,
                 **kwargs):
        super(ClientApp, self).__init__(**kwargs)
        self.screen_history = []
        self.collection_ctrl = collection_ctrl
        self.profile_ctrl = profile_ctrl
        self.search_ctrl = search_ctrl
        self.trade_ctrl = trade_ctrl

    def go_back(self, *args):
        if self.screen_history:
            sc = self.screen_history.pop()
            t = self.root.transition
            self.root.transition = FallOutTransition()
            self.root.current = sc
            self.root.transition = t
    
    def get_back_button(self):
        return (self.go_back, self.button_icons['back'])

    def build(self):
        self.icon = 'res/icon.png'
        self.title = 'Gemmarium'

        signup = SignupScreen(name='signup')
        menu = MenuScreen(name='menu')
        collection = CollectionScreen(name='collection')
        request = RequestScreen(name='request')
        search = SearchScreen(name='search')
        trade_list = TradeListScreen(name='trade_list')

        sm = ScreenManager(transition=CardTransition())
        if not self.profile_ctrl.is_logged_in():
            sm.add_widget(signup)
        sm.add_widget(menu)
        sm.add_widget(collection)
        sm.add_widget(request)
        sm.add_widget(search)
        sm.add_widget(trade_list)
        return sm
    
    def on_start(self):
        icons = Image('res/buttons.png')
        tx = icons.texture
        tx.mag_filter = 'nearest'
        self.button_icons = {
            'back': TextureRegion(0, 16, 16, 16, tx),
            'edit_offered': TextureRegion(16, 16, 16, 16, tx),
            'edit_wanted': TextureRegion(32, 16, 16, 16, tx),
            'trade': TextureRegion(48, 16, 16, 16, tx),
            'reject': TextureRegion(0, 0, 16, 16, tx),
            'accept': TextureRegion(16, 0, 16, 16, tx),
            'fusion': TextureRegion(32, 0, 16, 16, tx),
        }
        self.gem_base = Image('res/base.png').texture
        self.gem_base.mag_filter = 'nearest'
