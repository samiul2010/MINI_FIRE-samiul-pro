[app]
# (required) আপনার অ্যাপ্লিকেশনের নাম
title = Free Fire Mobile

# (required) প্যাকেজের নাম (সাধারণত ছোট হাতের অক্ষরে)
package.name = freefiremobile

# (required) প্যাকেজের ডোমেইন (সাধারণত উল্টো ডোমেইন নাম)
package.domain = org.samiul.ffmobile

# (required) সোর্স কোডের ডিরেক্টরি
source.dir = .

# (list) যে ধরনের ফাইলগুলো প্যাকেজে অন্তর্ভুক্ত হবে
source.include_exts = py,png,jpg,kv,atlas,db,ttf,json

# (str) আপনার অ্যাপ্লিকেশনের ভার্সন
version = 1.0

# (list) প্রয়োজনীয় লাইব্রেরি
# pyjnius অ্যান্ড্রয়েডের Java ক্লাস ব্যবহারের জন্য এবং sqlite3 ডাটাবেসের জন্য
requirements = python3,kivy==2.2.1,pyjnius,sqlite3

# (str) অ্যাপ চালু হওয়ার আগের স্প্ল্যাশ স্ক্রিনের রঙ (হেক্স কোড)
presplash.background_color = #000000

# (str) অ্যাপের আইকন (প্রয়োজনে একটি icon.png ফাইল তৈরি করে এখানে পাথ দিন)
# icon.filename = %(source.dir)s/icon.png

# (str) স্ক্রিনের দিক (portrait বা landscape)
orientation = portrait

# (bool) অ্যাপ্লিকেশনটি ফুলস্ক্রিন হবে কিনা
fullscreen = 0

[buildozer]
# (int) লগ লেভেল (0 = error, 1 = info, 2 = debug)
# ডিবাগ করার জন্য 2 ব্যবহার করা ভালো
log_level = 2

# (int) রুট ইউজার দিয়ে চালালে সতর্কবার্তা দেখাবে
warn_on_root = 1

# --------------------------------------------------
# Android এর জন্য নির্দিষ্ট সেটিংস (আধুনিক এবং সামঞ্জস্যপূর্ণ)
# --------------------------------------------------

# (int) টার্গেট অ্যান্ড্রয়েড API লেভেল (সর্বশেষ স্থিতিশীল)
android.api = 34

# (int) সর্বনিম্ন অ্যান্ড্রয়েড API লেভেল
android.minapi = 24

# (list) প্রয়োজনীয় পারমিশন
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (list) যে আর্কিটেকচারের জন্য বিল্ড হবে
android.archs = arm64-v8a, armeabi-v7a

# (str) অ্যান্ড্রয়েড NDK (Native Development Kit) এর ভার্সন
# 26c একটি আধুনিক এবং স্থিতিশীল পছন্দ
android.ndk = 26c

# (str) python-for-android এর ব্রাঞ্চ
# master ব্রাঞ্চে লেটেস্ট ফিক্সগুলো থাকে
p4a.branch = main

# (bool) রিলিজ বিল্ডের জন্য বিভক্ত AAB তৈরি করবে কিনা
# গুগল প্লে স্টোরে আপলোড করার জন্য এটি True রাখুন
android.release.build_aab = true

# --- Start.io Ad SDK ইন্টিগ্রেশন ---
# Gradle এর মাধ্যমে SDK যোগ করা
android.gradle_dependencies = 'com.startapp:inapp-sdk:4.11.+'

# AndroidManifest.xml ফাইলে আপনার App ID যোগ করা
# !!! আপনার আসল Start.io App ID এখানে ব্যবহার করুন !!!
android.manifest.meta-data = com.startapp.sdk.APPLICATION_ID=207965871

# AndroidManifest.xml এর application ট্যাগে অতিরিক্ত এন্ট্রি যোগ করা
# বিজ্ঞাপনের জন্য নেটওয়ার্ক অ্যাক্সেস নিশ্চিত করতে
android.manifest.application_tags =
    android:usesCleartextTraffic="true"

