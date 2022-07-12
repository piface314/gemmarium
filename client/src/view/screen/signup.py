from ctrl.profile import ProfileCtrl
from kivy.app import App
from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from view.component.popup import Loading, Warning
from exceptions import *
import threading

Builder.load_file('src/view/screen/signup.kv')


class SignupScreen(Screen):
        
    @mainthread
    def goto_menu(self):
        self.manager.current = 'menu'

    def signup(self):
        loading = Loading()
        loading.open()
        t = self.ids['text_input'].text
        worker = threading.Thread(target=self.resolve, args=(loading, t))
        worker.start()

    @mainthread
    def show_warning(self, msg):
        popup = Warning(msg)
        popup.open()
    
    def resolve(self, loading, t):
        try:
            ctrl: ProfileCtrl = App.get_running_app().profile_ctrl
            ctrl.signup(t)
            self.goto_menu()
        except UsernameTakenError:
            self.show_warning("Nome de usuário já cadastrado!")
        except InvalidUsernameError:
            self.show_warning("Nome de usuário inválido!\nApenas letras, dígitos, hífen, ponto e travessão são caracteres permitidos.")
        except Exception:
            self.show_warning("Erro desconhecido.")
        finally:
            loading.dismiss()
            
    
    
    

    
    