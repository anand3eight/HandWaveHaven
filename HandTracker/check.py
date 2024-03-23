import osascript
target_volume = 0
vol = "set volume output volume " + str(target_volume)
osascript.osascript(vol)

# or
target_volume = 0
osascript.osascript("set volume output volume {}".format(target_volume))

# or
osascript.osascript("set volume output volume 0")
print(osascript.osascript('get volume settings'))