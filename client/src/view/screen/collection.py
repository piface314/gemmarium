from ctrl.collection import CollectionCtrl
from kivy.app import App
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from model.gem import Gem
from view.component.holder import GemHolder

Builder.load_file('src/view/screen/collection.kv')


class CollectionScreen(Screen):

    gems = ListProperty([])
    
    def on_enter(self, *args):
        super().on_enter(*args)
        app = App.get_running_app()
        self.ctrl: CollectionCtrl = app.collection_ctrl
        self.gems = self.ctrl.list_gems()

    def goto_offered(self, *args):
        self.manager.current = 'offered'

    def goto_wanted(self, *args):
        self.manager.current = 'wanted'

    def goto_gem(self, gem: Gem):
        popup = Factory.GemShow()
        popup.title = gem.name
        popup.text = self.gem_text(gem)
        layout = popup.ids['layout']
        layout.add_widget(GemHolder.from_gem(gem), 1)
        popup.open()
    
    def gem_text(self, gem: Gem):
        lines = [
            f'Obtida em: {gem.obtained_at.strftime("%Y/%m/%d %H:%M:%S")}',
            f'Criada em: {gem.created_at.strftime("%Y/%m/%d %H:%M:%S")}',
            f'Criada para: @{gem.created_for}',
            f'Criada por: {gem.created_by}',
            f'Descrição:\n{gem.desc}'
        ]
        return '\n'.join(lines)

    def on_gems(self, _, gems):
        layout = self.ids['gem_list']
        layout.clear_widgets()
        for gem in gems:
            holder = GemHolder.from_gem(gem, True)
            holder.bind(on_release=lambda *_, g=gem: self.goto_gem(g))
            layout.add_widget(holder)
