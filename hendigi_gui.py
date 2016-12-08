#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import time
import os

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

hmi_state = 0
HOME_STATE = 0
PRVIEW_STATE = 1

# for GUI from here------
pygame.init()
pygame.mouse.set_visible(0)

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print ("Framebuffer size: %d x %d" % (size[0], size[1]))
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
title_font = pygame.font.Font(os.path.join('./keifont.ttf'), 48)
body_font = pygame.font.Font(os.path.join('./keifont.ttf'), 32)
# ----------- GUI

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    label=body_font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, (255,255,255), (xpo-10,ypo-10,width,height),3)

def on_touch_home():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 150 and 30 <= touch_pos[1] <=85:
        print ("auto")

    # button 2 event
    if 180 <= touch_pos[0] <= 330 and 30 <= touch_pos[1] <=85:
        print ("manual")

def screen_clear():
    screen.fill((0,0,0))
    pygame.display.update()

def screen_opening():
    title = title_font.render(u"変デジカメラ", True, (180,0,0))
    screen.fill((0,230,0))
    screen.blit(title, (30,100))
    pygame.display.update()
    time.sleep(3)
    screen_clear()

def screen_shutter():
    text = title_font.render(u"撮影中", True, (180,0,0))
    screen.fill((0,230,0))
    screen.blit(text, (50,100))
    pygame.display.update()

def screen_nophoto():
    text = title_font.render(u"写真無いよ", True, (180,0,0))
    screen.fill((0,230,0))
    screen.blit(text, (30,100))
    pygame.display.update()

def screen_home():
    global hmi_state
    hmi_state = HOME_STATE

    screen.fill((0,230,0))
    # screen.blit(title, (20,100))
    # make_button("auto", 30, 30 ,55, 120, (180, 0, 0))
    # make_button("manual", 180, 30 ,55, 120, (180, 0, 0))
    auto_text = body_font.render(u"おーと", True, (180,0,0))
    # ir_text = body_font.render(u"せきがいせん", True, (180,0,0))
    ai_text = body_font.render(u"じんこうちのう", True, (180,0,0))
    preview_text = body_font.render(u"ぷれびゅー", True, (180,0,0))
    end_text = body_font.render(u"おしまい", True, (180,0,0))
    screen.blit(auto_text,(100,30))
    # screen.blit(ir_text,(100,30))
    screen.blit(ai_text,(100,80))
    screen.blit(preview_text,(100,130))
    screen.blit(end_text,(100,180))
    pygame.display.update()

def screen_countup():
    count = 0
    while count <= 100:
        count_str = str(count) + "%"
        count_text = title_font.render(count_str, True, (180,0,0))
        screen.fill((0,230,0))
        screen.blit(count_text,(100,100))
        pygame.display.update()
        time.sleep(8)
        count += 10

def screen_preview(filename):
    global hmi_state
    hmi_state = PRVIEW_STATE

    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    screen.blit(img, (0,0))
    pygame.display.update()

if __name__ == '__main__':
    pass
# from here memo
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         print "screen pressed" #for debugging purposes
        #         pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
        #         print pos #for checking
        #         pygame.draw.circle(screen, (255,255,255), pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
        #         if hmi_state == home_menu:
        #             on_touch_home()
        #         if hmi_state == manual_menu:
        #             pass
        #         if hmi_state == ir_menu:
        #             pass
        #         if hmi_state == ai_menu:
        #             pass
        #
        #     #ensure there is always a safe way to end the program if the touch screen fails
        #     if event.type == KEYDOWN:
        #         if event.key == K_ESCAPE:
        #             sys.exit()
        # pygame.display.update()
