---------------------------------------------------------------------------
Installation guide/setup for Carnova android version
---------------------------------------------------------------------------
1. Download [Node.js](https://nodejs.org/en/)
2. Download [Android Studio](https://developer.android.com/studio)
3. Download [JDK 8](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
4. Download [Python 2](https://www.python.org/downloads/)
5. Download [Gradle](https://gradle.org/install/)
6. For Windows, press start, search for edit the system variables
- Select edit system variable
- Select Path under variable and press edit
- press add new 
- Add the following
```
C:\Program Files\Java\jdk1.8.0_221\bin
C:\<android installed location>\tools
C:\<android installed location>\tools\bin
C:\<android installed location>\platform-tools
C:\<android installed location>\build-tools
C:\<android installed location>\emulator
C:\<grandle installed location>\gradle-5.6.2\bin
C:\Python27
```
7. Check the enviroment variable are set properly. Open cmd.
Enter the following: python --version
```
Python 2.7.15
```
Gradle -v

```
Gradle 5.6.2
------------------------------------------------------------

Build time:   2019-09-05 16:13:54 UTC
Revision:     55a5e53d855db8fc7b0e494412fc624051a8e781

Kotlin:       1.3.41
Groovy:       2.5.4
Ant:          Apache Ant(TM) version 1.9.14 compiled on March 12 2019
JVM:          1.8.0_221 (Oracle Corporation 25.221-b11)
OS:           Windows 10 10.0 amd64
```

8. open cmd, find a location to save the project.
```
 cd C:\Users\xxxx\Desktop
 git clone https://github.com/AngXingLong/ict2x01-2019t1-team16.git
 npm install
 npm install -g cordova
```
9. Start the android simulator/ plug in your android phone. (please ensure usb debugging mode is **turned on**)
10. If plugging in your own phone, make sure the phone is detected. type adb devices
```
List of devices attached
Myphone
```
11. Run the application
'''
cordova run android
'''
