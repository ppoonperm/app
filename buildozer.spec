[app]
# ข้อมูลแอป
title = Personal Financial App
package.name = financialapp
package.domain = com.yourname.financialapp

# ไฟล์และโฟลเดอร์
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,json

# เวอร์ชัน
version = 1.0
version.regex = __version__ = ['"]([^'"]*)['"]
version.filename = %(source.dir)s/main.py

# Dependencies ที่ปรับปรุงแล้ว
requirements = python3==3.9.16,kivy==2.1.0,kivymd==1.1.1,sqlite3,pandas==1.5.3,plyer==2.1.0,pillow==9.5.0,requests==2.31.0,certifi

# ไอคอนและ presplash
#icon.filename = %(source.dir)s/data/icon.png
#presplash.filename = %(source.dir)s/data/presplash.png

# Orientation
orientation = portrait

# Services (สำหรับ background tasks)
#services = myservice:./service/main.py

# OSX Specific
#osx.python_version = 3
#osx.kivy_version = 1.9.1

[buildozer]
# Log level (0 = เฉพาะ error, 1 = info, 2 = debug)
log_level = 2

# Buildozer cache directory
warn_on_root = 1

[android]
# Android SDK/NDK versions ที่เสถียร
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Build tools
android.gradle_dependencies = 

# Java build options
android.add_java_dir = ./src/main/java

# Android permissions
permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# Android application meta-data
android.meta_data = 

# Android library project
#android.library_references = 

# Android logcat filters
android.logcat_filters = *:S python:D

# Copy library dependencies from the main application
#android.copy_libs = 1

# The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# In past, was `android.arch` as we weren't supporting builds for multiple archs at the same time.
android.archs = arm64-v8a, armeabi-v7a

# Allow backup of app data
android.allow_backup = True

# Indicate if the application should be fullscreen or not
fullscreen = 0

# Adaptive icon
#android.adaptive_icon.background = #FFFFFF
#android.adaptive_icon.foreground = %(source.dir)s/data/icon_fg.png

# Gradle repositories
android.gradle_repositories = google(), mavenCentral()

# Entry point
android.entrypoint = org.kivy.android.PythonActivity

# Custom source folders for requirements
# android.add_src = 

# Whitelist file extensions for APK packaging
#android.whitelist_src = py,png

# Black list for exclusion from APK
#android.blacklist_src = 

# Exclude file patterns
#android.exclude_patterns = license,images/*/*.jpg

# (list) Android application meta-data to set (key=value format)
# android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy

# (list) Android library project to add (will be added in the
# project.properties automatically.)
# android.library_references = @jar/my-android-library.jar

# (str) Rename the main activity (android.entrypoint)
# android.activity_class_name = org.kivy.android.PythonActivity

# Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# Port number to configure Kivy to start the app with
# p4a.port = 

# Private volume size
# android.private_volume_size = 

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes =

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to configure Kivy to start the app with
# p4a.port =

# Control passing the --private volume to the bootstrap
# p4a.private_volume =

# (str) Argument for --storage-dir
# p4a.storage_dir =

# (str) Argument for --ndk-dir
# p4a.ndk_dir =

# (str) Argument for --sdk-dir  
# p4a.sdk_dir =

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.manifest.intent_filters =

# (str) launchMode to set for the main activity
# android.manifest.launch_mode = standard

# (list) Android additional libraries to copy into libs/armeabi
# android.add_libs_armeabi = libs/android/*.so
# android.add_libs_armeabi_v7a = libs/android-v7/*.so
# android.add_libs_arm64_v8a = libs/android-v8/*.so
# android.add_libs_x86 = libs/android-x86/*.so
# android.add_libs_mips = libs/android-mips/*.so

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
# android.wakelock = False

# (list) Android application meta-data to set (key=value format)
# android.meta_data = 

# (list) Android library project to add (will be added in the
# project.properties automatically.)
# android.library_references = @jar/my-android-library.jar

# (list) Android shared libraries which will be added to android.app_mode
# sharedLibrary sections in the
# project.properties automatically.)
# android.shared_libraries =

# (str) Android entry point, default is org.kivy.android.PythonActivity
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
# It should be a subclass of PythonService class.
# android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme, default is depending on SDK version.
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
# android.whitelist = 

# (str) Path to a custom whitelist file
# android.whitelist_src = 

# (str) Path to a custom blacklist file
# android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so they can be imported.
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_java_dir = 

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) OUYA Console category. Should be one of GAME or APP
# If you leave this blank, OUYA support will not be enabled
# ouya.category = GAME

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
# ouya.icon.filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file to include as an intent filters in <activity> tag
# android.manifest.intent_filters = 

# (str) launchMode to set for the main activity
# android.manifest.launch_mode = standard

# (bool) Indicate whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if you set this to True
# android.wakelock = False

# (list) Android application meta-data to set (key=value format)
# android.meta_data = 

# (bool) Indicate whether the app should use the kivy metrics
# android.use_kivy_metrics = False

# Python for android (p4a) specific

# (str) python-for-android fork to use in case if you want to use a fork, defaults to upstream (kivy)  
# p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
# p4a.commit = HEAD

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
# p4a.source_dir = 

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes = 

# (str) Filename to the hook for p4a
# p4a.hook = 

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

# (int) port number to configure Kivy to start the app with
# p4a.port = 

# Control passing the --private volume to the bootstrap
# p4a.private_volume = 

# (str) Argument for --storage-dir
# p4a.storage_dir = 

# (str) Argument for --ndk-dir
# p4a.ndk_dir = 

# (str) Argument for --sdk-dir
# p4a.sdk_dir = 

# (bool) Use --private data storage (True) or --dir public storage (False)
# p4a.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
# android.sdk_path = 

# (str) ANT directory (if empty, it will be automatically downloaded.)
# android.ant_path = 

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
# android.accept_sdk_license = False

# (str) Android entry point, default is org.kivy.android.PythonActivity
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Android Activity
# It should be a subclass of either Activity or ActionBarActivity class.
# android.activity_class_name = org.kivy.android.PythonActivity

# (str) Full name including package path of the Java class that implements Python Service
# It should be a subclass of PythonService class.
# android.service_class_name = org.kivy.android.PythonService

# (str) Android app theme, default is depending on SDK version.
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
# android.whitelist = 

# (str) Path to a custom whitelist file
# android.whitelist_src = 

# (str) Path to a custom blacklist file
# android.blacklist_src = 

# (list) List of Java .jar files to add to the libs so they can be imported.
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_java_dir = 

# (str) Copies of license agreements  
# android.license_agreement = 

# (str) Path to the Android resource
# android.res_dir =