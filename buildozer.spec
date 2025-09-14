[app]
title = MINI FIRE
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow
android.ndk_api = 24
android.ndk = 25b
icon.filename = %(source.dir)s/data/icon.png
orientation = portrait
android.permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.allow_backup = True
p4a.branch = master
p4a.fork = kivy
android.copy_libs = 1
android.accept_sdk_license = True

# Start.io App ID (REPLACE WITH YOUR ACTUAL START.IO APP ID, e.g., '123456789')
android.meta_data = com.startapp.sdk.APPLICATION_ID="207965871"

[buildozer]
log_level = 2
warn_on_root = 1
