[app]
# (required) Title of your application
title = MINI FIRE 

# (required) Package name
package.name = minifiremobileapp

# (required) Package domain (usually reversed domain name)
package.domain = org.example.ffmobile

# (required) Source code directory
source.dir = .

# (list) Source files to include (let buildozer find them)
source.include_exts = py,png,jpg,kv,atlas,db,ttf,json

# (str) Version of your application
version = 1.0

# (list) Application requirements
# pyjnius for android java access, sqlite3 for the database
requirements = python3,kivy==2.2.1,pyjnius,sqlite3

# (str) Presplash background color (hex format)
presplash.background_color = #000000

# (str) Presplash image
# presplash.filename = data/presplash.png

# (str) Application icon
icon.filename = icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

[buildozer]
# (int) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Warn if running buildozer with root privileges
warn_on_root = 1

# --------------------------------------------------
# Android specific settings
# --------------------------------------------------

# (int) Android API to use
android.api = 33

# (int) Minimum API required
android.minapi = 24

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (list) Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Android NDK version to use
# Using a specific, known-stable version is better
android.ndk = 25b

# (str) Android SDK version
android.sdk = 20

# (str) Python for android branch to use
# Using 'master' is often more up-to-date
p4a.branch = master

# --- Start.io Ad SDK Integration ---
# Add Start.io SDK from Gradle
android.gradle_dependencies = 'com.startapp:inapp-sdk:4.11.+'

# Add the App ID to the AndroidManifest.xml
# !!! আপনার আসল Start.io App ID এখানে দিন !!!
android.manifest.meta-data = com.startapp.sdk.APPLICATION_ID=207965871

# Add required entries to the application tag in AndroidManifest.xml
android.manifest.application_tags =
    android:usesCleartextTraffic="true"
    
