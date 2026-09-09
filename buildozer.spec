[app]
title = Barkod Klasor
package.name = barkodklasor
package.domain = org.kanka
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy==2.2.1,camera4kivy,gestures4kivy,pyzbar,pillow
orientation = portrait
fullscreen = 0
android.permissions = CAMERA
p4a.hook = camerax_provider/gradle_options.py
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 0
