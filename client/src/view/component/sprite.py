from functools import reduce
from io import BytesIO
from kivy.animation import Animation
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import TextureRegion
from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.image import Image
from model.gem import Gem
from math import floor

Builder.load_file('src/view/component/sprite.kv')
gem_rects = [(16*i, 0, 16, 16) for i in range(8)]
logo_rects = [(0, 56*i, 168, 56) for i in range(6, -1, -1)]  \
    + [(168, 56*i, 168, 56) for i in range(6, -1, -1)]


def get_animation(frames=8, d0=1, dt=0.1):
    anim = Animation(frame=0, duration=d0)
    anim = reduce(lambda a, f: a + Animation(frame=f, duration=dt),
        range(1, frames), anim)
    return anim + Animation(frame=0, duration=0)

def get_bytes_sheet(image, rects, filename=None):
    data = BytesIO(image)
    im = CoreImage(data, ext='png', filename=filename)
    im.texture.mag_filter = 'nearest'
    return [TextureRegion(x, y, w, h, im.texture)
        for x, y, w, h in rects]

def get_file_sheet(source, rects):
    im = CoreImage(source)
    im.texture.mag_filter = 'nearest'
    return [TextureRegion(x, y, w, h, im.texture)
        for x, y, w, h in rects]

class Sprite(Image):

    frame = NumericProperty(-1)
    animate = BooleanProperty(False)
    sheet = ListProperty([])
    animation = ObjectProperty(None)

    @classmethod
    def from_bytes(cls, image, rects, filename=None, **kwargs):
        sheet = get_bytes_sheet(image, rects, filename)
        anim = get_animation(len(rects))
        return cls(animation=anim, sheet=sheet, **kwargs)

    @classmethod
    def from_gem(cls, gem: Gem):
        return cls.from_bytes(gem.sprite, gem_rects, f'{gem.id}.png')

    def on_sheet(self, *_):
        self.frame = 0

    def get_sprite_frame(self, frame):
        i = floor(frame)
        return self.sheet[i] if 0 <= i < len(self.sheet) else None

    def on_animate(self, _, value):
        if value:
            self.animation.repeat = True
            self.animation.start(self)
        else:
            self.animation.cancel(self)
            self.frame = 0
