from functools import reduce
from io import BytesIO
from kivy.animation import Animation
from kivy.core.image import Image as CoreImage
from kivy.graphics.texture import TextureRegion
from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.image import Image
from math import floor

Builder.load_file('src/view/component/sprite.kv')
gem_rects = [(16*i, 0, 16, 16) for i in range(8)]
logo_rects = [(0, 56*i, 168, 56) for i in range(6, -1, -1)]  \
    + [(168, 56*i, 168, 56) for i in range(6, -1, -1)]


class Sprite(Image):
    @staticmethod
    def sprite_anim(frames=8, d0=1, dt=0.1):
        anim = Animation(frame=0, duration=d0)
        anim = reduce(lambda a, f: a + Animation(frame=f, duration=dt),
            range(1, frames), anim)
        return anim + Animation(frame=0, duration=0)

    frame = NumericProperty(0)
    animate = BooleanProperty(False)
    sheet = ListProperty([])
    anim = ObjectProperty(None)

    @classmethod
    def from_bytes(cls, image, rects, filename=None, **kwargs):
        data = BytesIO(image)
        im = CoreImage(data, ext='png', filename=filename)
        im.texture.mag_filter = 'nearest'
        sheet = [TextureRegion(x, y, w, h, im.texture)
            for x, y, w, h in rects]
        anim = cls.sprite_anim(len(sheet))
        return cls(anim=anim, sheet=sheet, **kwargs)
    
    @classmethod
    def from_file(cls, source, rects, **kwargs):
        im = CoreImage(source)
        im.texture.mag_filter = 'nearest'
        sheet = [TextureRegion(x, y, w, h, im.texture)
            for x, y, w, h in rects]
        anim = cls.sprite_anim(len(sheet))
        return cls(anim=anim, sheet=sheet, **kwargs)

    def get_sprite_frame(self, frame):
        return self.sheet[floor(frame)]

    def on_animate(self, _, value):
        if value:
            self.anim.repeat = True
            self.anim.start(self)
        else:
            self.anim.cancel(self)
            self.frame = 0
