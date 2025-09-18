[app]
title = Mini Fire
package.name = minifire
package.domain = org.kivy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json
version = 1.0
requirements = python3,kivy,pyjnius
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Android API
android.api = 24
android.minapi = 21
android.arch = arm64-v8a

# Start.io SDK যোগ করা
android.gradle_dependencies = com.startapp:inapp-sdk:5.+

# Custom AndroidManifest যোগ করার জন্য
android.add_src = src
