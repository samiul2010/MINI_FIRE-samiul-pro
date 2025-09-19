[app]

title = Mini Fire
package.name = minifire
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0
android.accept_sdk_license = True
android.api = 24
android.minapi = 21
android.archs = arm64-v8a   # ✅ Play Store ready (64-bit)

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Start.io Ads SDK dependency
android.gradle_dependencies = com.startapp:inapp-sdk:5.+

# যদি আপনার custom java code থাকে
android.add_src = src

# Icon
icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
