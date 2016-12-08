#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import pigpio
import syslog
import socket
import shutter as sh
import hendigi_gui as gui

host = "karaage.local"
port = 8888

# global
SleepStepSec = 0.1

preview_numb = 0

loop = True

# gpio
pi = pigpio.pi()
pi.set_mode(17, pigpio.INPUT)
pi.set_mode(22, pigpio.INPUT)
pi.set_mode(23, pigpio.INPUT)
pi.set_mode(27, pigpio.INPUT)
pi.set_pull_up_down(17, pigpio.PUD_UP)
pi.set_pull_up_down(22, pigpio.PUD_UP)
pi.set_pull_up_down(23, pigpio.PUD_UP)
pi.set_pull_up_down(27, pigpio.PUD_UP)

# for socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def go_home():
    global preview_numb
    preview_numb = sh.shutter_numb
    gui.screen_home()

def cb_shutter(gpio, level, tick):
    print (gpio, level, tick)
    if KeepWatchForSeconds(1, gpio):
        if gui.hmi_state == gui.PRVIEW_STATE:
            go_home()
        else:
            gui.screen_shutter()
            sh.cameraLoad()
            # sh.shutter()
            sh.shutter_small()
            sh.cameraSave()
            go_home()

def cb_ir(gpio, level, tick):
    print (gpio, level, tick)
    if KeepWatchForSeconds(1, gpio):
        print("ir")
        pass

def cb_ai(gpio, level, tick):
    print (gpio, level, tick)
    if KeepWatchForSeconds(1, gpio):
        if gui.hmi_state == gui.PRVIEW_STATE:
            go_home()
        else:
            gui.screen_shutter()
            sh.cameraLoad()
            sh.shutter_small()
            sh.cameraSave()
            print ("ai")
            ai_photo()
            go_home()
            gui.screen_home()

def cb_preview(gpio, level, tick):
    print (gpio, level, tick)
    if KeepWatchForSeconds(0.5, gpio):
        preview()

def cb_shutdown(gpio, level, tick):
    print (gpio, level, tick)
    if KeepWatchForSeconds(3, gpio):
        print("shutdown")
        if gui.hmi_state == gui.PRVIEW_STATE:
            go_home()
        else:
            # global loop
            # loop = False
            CallShutdown()

def ai_photo():
    client.send("go")
    rcvmsg = client.recv(4096)
    print rcvmsg
    if rcvmsg == 'ok':
        client.send(str("{0:06d}".format(sh.shutter_numb) + ".jpg"))

        response = client.recv(4096)
        print (response)

        gui.screen_countup()
        client.send("count_full")
        response = client.recv(4096)
        print (response)
        response = client.recv(4096)
        print (response)

def KeepWatchForSeconds(seconds, pin_numb):
    GoFlag = True
    # if seconds < 1:
        # seconds = 1
    while seconds > 0:
        time.sleep(SleepStepSec)
        seconds -= SleepStepSec
        if (pi.read(pin_numb) == True):
            GoFlag = False
            break
    return GoFlag

def CallShutdown():
    print("Going shutdown by GPIO.")
    syslog.syslog(syslog.LOG_NOTICE, "Going shutdown by GPIO.")
    os.system("/sbin/shutdown -h now 'Poweroff by GPIO'")

def preview():
    print ("preview")
    if preview_numb == 0:
        gui.screen_nophoto()
    else:
        global preview_numb
        filename = os.path.join(sh.photo_dir, str("{0:06d}".format(preview_numb)) + '.jpg')
        gui.screen_preview(filename)

        preview_numb -= 1
        if preview_numb < 1:
            preview_numb = sh.shutter_numb

# cb1 = pi.callback(17, pigpio.FALLING_EDGE, cb_ir)
cb1 = pi.callback(17, pigpio.FALLING_EDGE, cb_shutter)
cb2 = pi.callback(22, pigpio.FALLING_EDGE, cb_ai)
cb3 = pi.callback(23, pigpio.FALLING_EDGE, cb_preview)
cb4 = pi.callback(27, pigpio.FALLING_EDGE, cb_shutdown)

if __name__ == '__main__':
    sh.photodirCheck()

    if not pi.connected:
        exit()

    sh.cameraLoad()
    preview_numb = sh.shutter_numb

    gui.screen_opening()

    gui.screen_home()

    while loop == True:
        pass

    # try:
          # GPIO.wait_for_edge(UpSw, GPIO.FALLING)
    # except KeyboardInterrupt:
         # GPIO.cleanup()  # clean up GPIO on CTRL+C exit
    # GPIO.cleanup()

