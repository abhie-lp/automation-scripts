# batch_scripts

Add the folder to Path in environment variables

1. [adb take screenshot](#adb-take-screenshot)
2. [scrcpy to record](#scrcpy-to-record)
3. [send a desktop notification](#send-a-desktop-notification)

* * *

##### adb take screenshot
- Take screenshot of the device's current screen.
- Optional parameters provided
    - -s/--serial: Android device's serial ID
    - -f/--filename: Filename that is to be added as suffix after date_time
    - -d/--device: Name of the device whose id will be fetched from terminal variable or environment variable
```
adb_ss

adb_ss -s casd234234 -f test

set r5=casd234234
adb_ss -f test -d r5
```

##### scrcpy to record
- Start recording the Android device's screen
- Optional parameters
    - Optional parameters provided
    - -s/--serial: Android device's serial ID
    - -f/--filename: Filename that is to be added as suffix after date_time
    - -d/--device: Name of the device whose id will be fetched from terminal variable or environment variable

```
scpy_record

scpy_record -s sdeg34534dfg -f test_record

set mi11=sdeg34534dfg
scpy_record -d mi11
```

##### send a desktop notification
Send a desktop notification using **powershell**
```
notify.ps1 "It starts with one thing"
notify.ps1 "So i'm breaking the habit"
notify.ps1 "Let it go"
```