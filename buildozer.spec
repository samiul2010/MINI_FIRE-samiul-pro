[app]
# (str) Title of your application
title = Mini Fire
# (str) Package name (one word, no special chars)
package.name = mini_fire
# (str) Package domain (reverse-DNS style)
package.domain = org.kivy
# (str) Source code directory (where main.py lives)
source.dir = .
# (list) Include typical resource extensions
source.include_exts = py,png,jpg,kv,atlas

# (str) Application version
version = 1.0

# (list) Application requirements (Python modules)
# Based on imports: Kivy framework and pyjnius for Java calls
requirements = python3,kivy,pyjnius

# (list) Presplash (optional, skip if not used)
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Orientation (portrait or landscape; choose per app design)
orientation = portrait

# (bool) Fullscreen mode (hide status bar). 0 = disabled (show bar)
fullscreen = 0

# (list) Permissions (needed for network and storage access):contentReference[oaicite:1]{index=1}:contentReference[oaicite:2]{index=2}
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Android app meta-data (key=value format).
# Add Start.io (StartApp) Application ID as metadata:contentReference[oaicite:3]{index=3}.
# Replace YOUR_STARTAPP_APP_ID with your actual app ID.
android.meta_data = com.startapp.sdk.APPLICATION_ID=YOUR_STARTAPP_APP_ID

# (list) Android Gradle dependencies.
# Include the Start.io (StartApp) in-app SDK (via Maven Central):contentReference[oaicite:4]{index=4}.
android.gradle_dependencies = "com.startapp:inapp-sdk:5.+"

# (list) Android Gradle repositories.
# Ensure the StartApp Maven repository is available (if needed):contentReference[oaicite:5]{index=5}.
android.gradle_repositories = "mavenCentral()", "maven { url 'https://startappdev.bintray.com/maven' }"

# (str) Android API to use (target SDK; 24 as requested)
android.api = 24
# (int) Minimum API your APK will support (must be ≥21 for arm64-v8a):contentReference[oaicite:6]{index=6}
android.minapi = 21
# (int) Android NDK API (should match minapi for stability):contentReference[oaicite:7]{index=7}
android.ndk_api = 21

# (list) Android architectures to build (only 64-bit ARM as requested):contentReference[oaicite:8]{index=8}
android.archs = arm64-v8a

# (bool) Android auto backup feature (Android API ≥23)
android.allow_backup = True

[buildozer]
# (int) Log level (0=error only, 1=info, 2=debug)
log_level = 2
# (bool) Warn if run as root (0=no, 1=yes)
warn_on_root = 1
