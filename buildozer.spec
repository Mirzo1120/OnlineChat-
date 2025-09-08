[app]
title = OnlineChat
package.name = onlinechat
package.domain = org.example
source.include_exts = py,png,jpg,kv,json,ttf,mp3,ogg
version = 1.0.0
requirements = python3,kivy,requests,pillow,plyer,android,certifi,urllib3,chardet,idna,setuptools,firebase_admin
orientation = portrait
fullscreen = 1

# Permissions for media, camera, notifications, and storage
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE

# API and SDK settings
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# Architecture support
android.arch = armeabi-v7a,arm64-v8a,x86,x86_64

# Firebase messaging dependency
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.0.0

# Optional features
android.allow_backup = True
android.support = True
android.enable_multiprocessing = True
android.logcat_filters = *:S python:D

# Icon only (no presplash)
icon.filename = assets/icon.png

# Include .kv files and media assets
include_exts = py,kv,png,jpg,json,ttf,mp3,ogg

# Entry point
entrypoint = main.py

# Screenshots (optional, for Play Store)
# android.screenshots = screenshots/screen1.png,screenshots/screen2.png

# Package metadata
package.version_code = 1
package.version_name = 1.0.0

[buildozer]
log_level = 2
warn_on_root = 1
