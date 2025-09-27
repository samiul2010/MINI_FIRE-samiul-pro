ড[app]
title = MINI FIRE
package.name = minifire
package.domain = com.samiul
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,json
version = 1.0.0
requirements = 
    python3,
    kivy==2.1.0,
    android,
    jnius,
    sqlite3,
    openssl,
    requests,
    pillow,
    pyjnius

android.accept_sdk_license = True
# (str) python-for-android branch to use, defaults to master
p4a.branch = develop
[android]
api = 33
minapi = 21
permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[app:icon]
icon.filename = icon.png
[buildozer]
full_rebuild = 1
