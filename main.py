import config as cfg
import numpy as np
import subprocess
import keyboard
import json
import time
import cv2
import mss
import os
from os import path

def get_name():
	name = time.strftime("%Y.%m.%d - %H.%M.%S", time.localtime())
	return cfg.SAVE_PATH + name + cfg.FILE_EXTENSION

def exp_open():
	subprocess.Popen('explorer "' + cfg.SAVE_PATH + '"')

print("PyRec")
print("By xzxADIxzx")
print("V1.0 Release")
print()

# config
print("Loading config...")
expand_path = path.expandvars("%APPDATA%\\PyRec\\cfg.json")
if path.exists(expand_path):
	file = open(expand_path)
	load = json.load(file)
	file.close()
	cfg.SCREEN_SIZE = tuple(load["SCREEN_SIZE"])
	cfg.SAVE_PATH = load["SAVE_PATH"]
	cfg.FILE_EXTENSION = load["FILE_EXTENSION"]
	cfg.FOURCC_CODEC = load["FOURCC_CODEC"]
	cfg.HOTKEY_STOP = load["HOTKEY_STOP"]
	cfg.HOTKEY_PAUSE = load["HOTKEY_PAUSE"]
	cfg.HOTKEY_OPEN = load["HOTKEY_OPEN"]
else:
	with mss.mss() as sct:
		cfg.SCREEN_SIZE = (sct.monitors[0]["width"], sct.monitors[0]["height"])
	cfg.SAVE_PATH = path.expandvars("%USERPROFILE%\\Videos\\PyRec\\")
	cfg.FILE_EXTENSION = ".mp4"
	cfg.FOURCC_CODEC = "MP42"
	cfg.HOTKEY_STOP = "shift + s"
	cfg.HOTKEY_PAUSE = "shift + p"
	cfg.HOTKEY_OPEN = "shift + o"
	obj = { "SCREEN_SIZE": cfg.SCREEN_SIZE, "SAVE_PATH": cfg.SAVE_PATH, "FILE_EXTENSION": cfg.FILE_EXTENSION, "FOURCC_CODEC": cfg.FOURCC_CODEC,
			"HOTKEY_STOP": cfg.HOTKEY_STOP, "HOTKEY_PAUSE": cfg.HOTKEY_PAUSE, "HOTKEY_OPEN": cfg.HOTKEY_OPEN }
	if not path.exists(path.expandvars("%APPDATA%\\PyRec")):
		os.mkdir(path.expandvars("%APPDATA%\\PyRec"))
	file = open(expand_path, "w+")
	json.dump(obj, file, indent=4)
	file.close()

# record
print("Press [space] to start recording")
keyboard.wait("Space")
print("Press [" + cfg.HOTKEY_STOP + "] to stop recording or [" + cfg.HOTKEY_PAUSE + "] to pause")
print("Press [" + cfg.HOTKEY_OPEN + "] if you want to open the folder with recordings")
keyboard.add_hotkey(cfg.HOTKEY_OPEN, exp_open)
if not path.exists(cfg.SAVE_PATH):
	os.makedirs(cfg.SAVE_PATH)
vwf = cv2.VideoWriter_fourcc(*cfg.FOURCC_CODEC)
out = cv2.VideoWriter(get_name(), vwf, 24.0, cfg.SCREEN_SIZE)
mon = {'top': 0, 'left': 0, 'width': cfg.SCREEN_SIZE[0], 'height': cfg.SCREEN_SIZE[1]}
sct = mss.mss()
while True:
	img = sct.grab(mon)
	frm = np.array(img)
	out.write(frm)
	time.sleep(.01)

	if keyboard.is_pressed(cfg.HOTKEY_STOP):
		break

	if keyboard.is_pressed(cfg.HOTKEY_PAUSE):
		print("Press [" + cfg.HOTKEY_PAUSE + "] to continue...")
		keyboard.wait(cfg.HOTKEY_PAUSE)
		print("Recording...")
		time.sleep(.5 )

out.release()
print("Recording completed!")
input()