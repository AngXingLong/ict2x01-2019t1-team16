

## Introduction

GiaLey! is a cross-platform mobile application prototype that is built in collaboration between Singapore Institute of Technology (SIT) and Land Transport Authority (LTA) to improve the walking commute experience during the First Mile and Last Mile portion (FMLM) of their journey. GiaLey! is a gamified routing app that will comprise elements of a role playing game, route planner and a rewards marketplace. A “ Hero” is a representation of a user’s gameplay character. By clocking a certain number of steps during a user’s walking commute, users can stand a chance to unlock a random equipment, which can then be used to upgrade his Hero. Subsequently, the user can send his/her Hero on expeditions to gather H-Tokens (An ingame virtual currency). H-Tokens can be used to redeem rewards from the reward marketplace. GiaLey! will also recommend a variety FMLM routes between two points on a map, allowing users to discover new routes. Since this application is targeted at only the FMLM portion of the journey, routes recommendation will only be based on the FM and LM specified by the user.

## Video
URL NEEDED

## Installation Guide (User)
1. Download [gialey! moblie app.apk](https://github.com/AngXingLong/ict2x01-2019t1-team16/blob/master/gialey!%20moblie%20app.apk "gialey! moblie app.apk")
2. Open APK
3. Click on settings
4. Click on Enable unknown sources installation
5. Click Ok
6. Click Allow
7. Find and Start HelloCordova (GiaLey! App)

## Component Diagram
![component_diagram](/readmeImages/component_diagram.png)

## Installation Guide (Developer)
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
12. For more info refer to https://cordova.apache.org/docs/en/latest/guide/cli/#installing-the-cordova-cli

