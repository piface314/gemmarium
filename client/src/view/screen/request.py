from ctrl.collection import CollectionCtrl
from exceptions import QuotaError
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from model.gem import Gem
from view.component.popup import Loading, Warning
from view.component.sprite import Sprite, gem_rects
from view.component.holder import GemHolder
import threading

Builder.load_file('src/view/screen/request.kv')


class RequestScreen(Screen):

    gem = ObjectProperty(None)
    time = NumericProperty(None)
    button_disabled = BooleanProperty(False)
    msg = StringProperty("...")

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
    
    @staticmethod
    def format_time(s):
        h, s = s // 3600, s % 3600
        m, s = s // 60, s % 60
        return f'{h}:{m:02d}:{s:02d}'
    
    def request(self):
        self.msg = "..."
        loading = Loading()
        loading.open()
        worker = threading.Thread(target=self.resolve, args=(loading,))
        worker.start()

    def resolve(self, loading):
        try:
            app = App.get_running_app()
            ctrl: CollectionCtrl = app.collection_ctrl
            self.gem = ctrl.request_gem()
        except QuotaError as e:
            self.show_wait(e)
        except Exception:
            self.show_warning("Erro desconhecido.")
        finally:
            loading.dismiss()
    
    @mainthread
    def show_warning(self, msg):
        popup = Warning(msg)
        popup.open()
    
    @mainthread
    def show_wait(self, e):
        self.time = e.args[0]
        self.msg = "Cota de solicitação excedida! Espere um pouco..."
        self.button_disabled = True
        wl = Factory.WaitLabel()
        wl.text = self.format_time(self.time)
        layout = self.ids['display']
        layout.clear_widgets()
        layout.add_widget(wl)
        def update(_):
            if self.time > 0:
                self.time -= 1
                wl.text = self.format_time(self.time)
            else:
                layout.clear_widgets()
                self.msg = "..."
                self.button_disabled = False
                self.ev.cancel()
        self.ev = Clock.schedule_interval(update, 1)
    
    @mainthread
    def on_gem(self, _, val: Gem):
        if not val:
            return
        self.msg = f'Você ganhou: {val.name}!'
        gem = Sprite.from_bytes(
            val.sprite,
            gem_rects,
            f'{val.id}.png'
        )
        gem.animate = True
        gem.allow_stretch = True
        gem.size_hint = (0.5, 0.5)
        gem.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        app = App.get_running_app()
        holder = GemHolder(highlight=False)
        holder.ids['base'].texture = app.get_texture('base')
        holder.size_hint = (0.6, 0.6)
        holder.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        holder.add_widget(gem)
        layout = self.ids['display']
        layout.clear_widgets()
        layout.add_widget(holder)
            
