from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from model.gem import Gem
from view.component.sprite import Sprite, gem_rects

Builder.load_file('src/view/component/holder.kv')


class GemHolder(ButtonBehavior, RelativeLayout):
    
    highlight = BooleanProperty(False)

    @classmethod
    def from_gem(self, gem: Gem, highligh=False):
        gem_sp = Sprite.from_bytes(
            gem.sprite,
            gem_rects,
            f'{gem.id}.png'
        )
        gem_sp.animate = True
        gem_sp.allow_stretch = True
        gem_sp.size_hint = (0.5, 0.5)
        gem_sp.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        holder = GemHolder(highlight=highligh)
        holder.add_widget(gem_sp)
        return holder