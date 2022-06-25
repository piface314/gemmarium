from ctrl.collection import CollectionCtrl
from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from exceptions import QuotaError
from view.component.popup import Loading, Warning
import threading

Builder.load_file('src/view/screen/request.kv')


class RequestScreen(Screen):

    gem = ObjectProperty(None)
    time = NumericProperty(0)

    def on_enter(self, *args):
        app = App.get_running_app()
        bar = self.ids['header']
        bar.lt_btn = [app.get_back_button()]
    
    def request(self):
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
        popup = Warning("Cota de solicitação excedida!\nEspere um pouco...")
        popup.open()
        wl = Factory.WaitLabel()
        wl.text = str(self.time)
        layout = self.ids['display']
        layout.clear_widgets()
        layout.add_widget(wl)
        def update(_):
            if self.time > 0:
                self.time -= 1
                wl.text = str(self.time)
            else:
                layout.clear_widgets()
                self.ev.cancel()
        self.ev = Clock.schedule_interval(update, 1)
    
    @mainthread
    def on_gem(self, _, val):
        if val:
            print(val)
            
