[app]
# (str) Title of your application
title = Mini Fire

# (str) Package name
package.name = minifire

# (str) Package domain (reverse-DNS style)
package.domain = org.kivy

# (str) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
# (Python standard libs যেমন os, sys, sqlite3 ইত্যাদি আলাদা করে লিখতে হয় না)
requirements = python3,kivy,pyjnius,kivymd,pillow

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (list) Android meta-data
# ⚠️ আপনার আসল Start.io App ID দিয়ে নিচের placeholder বদলে দিন
android.meta_data = com.startapp.sdk.APPLICATION_ID=YOUR_STARTAPP_APP_ID

# (list) Gradle dependencies (Start.io SDK যোগ করা হলো)
android.gradle_dependencies = "com.startapp:inapp-sdk:5.+"

# (list) Gradle repositories
android.gradle_repositories = "mavenCentral()", "maven { url 'https://startappdev.bintray.com/maven' }"

# (int) Targeted Android API (workflow এ আমরা platforms;android-24 ইনস্টল করছি)
android.api = 24

# (int) Minimum API (arm64-v8a এর জন্য অন্তত 21 দরকার)
android.minapi = 21

# (int) Android NDK API (minsdk এর সাথে match করা জরুরি)
android.ndk_api = 21

# (list) Architectures to build (শুধু 64-bit ARM)
android.archs = arm64-v8a

# (bool) Allow app backup
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
