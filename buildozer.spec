[app]
# (required) আপনার অ্যাপ্লিকেশনের নাম
title = MINI FIRE

# (required) প্যাকেজের নাম
package.name = minifiremobile

# (required) প্যাকেজের ডোমেইন
package.domain = org.samiul.ffmobile

# (required) সোর্স কোডের ডিরেক্টরি
source.dir = .

# (list) যে ধরনের ফাইলগুলো প্যাকেজে অন্তর্ভুক্ত হবে
source.include_exts = py,png,jpg,kv,atlas,db,ttf,json

# (str) আপনার অ্যাপ্লিকেশনের ভার্সন
version = 1.0

# (list) প্রয়োজনীয় লাইব্রেরি
requirements = python3,kivy==2.2.1,pyjnius,sqlite3

# (str) অ্যাপ চালু হওয়ার আগের স্প্ল্যাশ স্ক্রিনের রঙ
presplash.background_color = #000000

# (str) অ্যাপের আইকন
# icon.filename = %(source.dir)s/icon.png

# (str) স্ক্রিনের দিক
orientation = portrait

# (bool) অ্যাপ্লিকেশনটি ফুলস্ক্রিন হবে কিনা
fullscreen = 0

# --------------------------------------------------
# Android এর জন্য নির্দিষ্ট সেটিংস (সঠিক সেকশনে)
# --------------------------------------------------

# (int) টার্গেট অ্যান্ড্রয়েড API লেভেল
android.api = 34

# (int) সর্বনিম্ন অ্যান্ড্রয়েড API লেভেল
android.minapi = 24

# (list) প্রয়োজনীয় পারমিশন
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (list) যে আর্কিটেকচারের জন্য বিল্ড হবে
android.archs = arm64-v8a, armeabi-v7a

# (str) অ্যান্ড্রয়েড NDK (Native Development Kit) এর ভার্সন
android.ndk = 26c

# (str) python-for-android এর ব্রাঞ্চ
p4a.branch = main

# (bool) রিলিজ বিল্ডের জন্য AAB তৈরি করবে কিনা
android.release.build_aab = true

# --- Start.io Ad SDK ইন্টিগ্রেশন ---
android.gradle_dependencies = 'com.startapp:inapp-sdk:4.11.+'
android.manifest.meta-data = com.startapp.sdk.APPLICATION_ID=207965871
android.manifest.application_tags =
    android:usesCleartextTraffic="true"


[buildozer]
# (int) লগ লেভেল (ডিবাগ করার জন্য 2)
log_level = 2

# (int) রুট ইউজার দিয়ে চালালে সতর্কবার্তা দেখাবে
warn_on_root = 1
