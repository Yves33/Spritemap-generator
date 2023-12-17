SpriteSheet splitter
====================

Small utility to isolate sprite rects from spritesheets.

1 - Requirements:
================
- OpenCV
- numpy
- pyglet is required to run the (minimal) demo

2 - Usage:
==========
```
python generate_spritemap.py myspritesheet.png
```
the program will generate (and show) 
- a json file with the rectangle coordinates of each individual sprite.
- a png file with the bounding boxes of the sprites and the sprite numbers

3 - Coordinate system:
======================
The program uses pyglet's coordinate system (up pointing y axis). If you need a down pointing y axis, you should edit the file generate_spritemap.py and change PYGLET_COORDINATES to False

A small demo is provided (requires pyglet library to run)

4 - License:
============
Te license is MIT. The provided sample spritesheet may not be free.