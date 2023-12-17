#!/bin/env python3
import json
import pyglet
from pyglet.gl import *
from pyglet.window import key

def loadsheet(im_file,region_file,spritenums=[]):
    spritesheet=pyglet.image.load(im_file)
    frames=[]
    rects=json.load(open(region_file,"r"))["rectangles"]
    if len(spritenums):
        rects=[rects[i] for i in spritenums]
    for rect in rects:
        pic=spritesheet.get_region(*rect)
        pic.anchor_x = pic.width // 2         ## center picture
        pic.anchor_y = pic.height // 2
        frames.append(pic)
    return frames

def loadanim(frames,imstack,dt,loop):
    return pyglet.image.Animation.from_image_sequence(
                [imstack[i] for i in frames],
                dt,
                True)

class playersprite(pyglet.sprite.Sprite):
    def __init__(self,images,x=0,y=0):
        super().__init__(list(images.values())[0],x,y)
        self.images=images
        self.current_image=list(images.keys())[0]
        self.alive=True
            
    def set_animation(self,anim):
        ## do not change animation if it's already set or you'll reset it
        if anim!=self.current_image:
            self.current_image=anim
            self.image=self.images[anim]
            
    def on_animation_end(self):
        if self.current_image=="die":
            self.delete()
            self.alive=False
        elif self.current_image in ["jump","walk","run"]:
            self.set_animation("idle")
            
STEP=6
game_window = pyglet.window.Window(640,480)
keys = key.KeyStateHandler()
game_window.push_handlers(keys)

@game_window.event
def on_draw():
    game_window.clear()
    player.draw()

def on_key_press(symbol, modifiers):
    if symbol==pyglet.window.key.J:
        player.set_animation("jump")
    if symbol==pyglet.window.key.W:
        player.set_animation("walk")
    if symbol==pyglet.window.key.R:
        player.set_animation("run")
    if symbol==pyglet.window.key.I:
        player.set_animation("idle")

def on_key_release(symbol, modifiers):
    pass

def on_mouse_press(x, y, button, modifiers):
    pass

def on_mouse_release(x, y, button, modifiers):
    pass

def on_mouse_motion(x, y, dx, dy):
    pass

def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    pass

def update(dt):
    if keys[key.UP]:
        player.y+=STEP
    if keys[key.DOWN]:
        player.y-=STEP
    if keys[key.LEFT]:
        player.x-=STEP
        player.set_animation("run")
        player.scale_x=-1.0
    if keys[key.RIGHT]:
        player.x+=STEP
        player.set_animation("run")
        player.scale_x=1.0

walk=[24,22,25,23,27,29,28,26,30,31,32]         ## individual frame numbers
jump=[51,52,53,54,57,58,49,50,55,56,59,60]      ## individual frame numbers
run=[41,42,44,46,48,47,45,43]                   ## individual frame numbers
idle=[17,18,19,20]                              ## individual frame numbers

image_list=loadsheet('./resource/megaman_full.png',
                     './resource/megaman_full.json')
walkanim=loadanim(walk,image_list,0.06,False)
jumpanim=loadanim(jump,image_list,0.06,False)
runanim=loadanim(run,image_list,0.06,False)
idleanim=loadanim(idle,image_list,0.1,True)

player=playersprite({"idle":idleanim,
                    "run":runanim,
                    "walk":walkanim,
                    "jump":jumpanim}
                    , game_window._width//2,game_window._height//2)

game_window.push_handlers(on_mouse_motion,
            on_key_press,
            on_key_release,
            on_mouse_drag,
            on_mouse_press,
            on_mouse_release,
            )

pyglet.clock.schedule_interval(update, 0.033)
pyglet.app.run()