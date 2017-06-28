# android-nougat-ssl-apk-patcher

### Requirements
Java JDK(tested on OpenJDK-8)

apksigner is included, but if shit starts breaking then install Android SDK and replace `java -jar apksigner.jar` with `apksigner` in patch.py.

### Usage
Copy the APK you would like to patch into the same directory as patch.py. Then run `python3 patch.py`. It will prompt you for the APK's name. Once finished, there will be a file called {apk name}\_signed.apk. This APK is fully patched and signed.

### Notes
* For reference, patching Instagram took 39 seconds. The majority of that time is APKTool decoding and building the APK
* This does not bypass certificate pinning

