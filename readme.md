# TiltR
Tilt controlls for **any** controller

## How does it work?
A webcam is used to track two markers on your controller.

## How do I install it?
### Linux:

#### 1. download this repository
```commandline
git clone https://github.com/treecaptcha/TiltR.git
```
#### 2. Install python packages
```commandline
pip3 install evdev
pip3 install opencv-contrib-python
```
note: this requires the python 3 version of pip, you may have to run `pip` instead of `pip3` on your distrubution.
#### 3. enter the directory
```commandline
cd TiltR
```
#### 4. start the script
```commandline
python3 main.py
```
note: this requires python 3, you may have to run `python` instead of `python3` on your distrubution.
#### 5. use commands to configure
```
list - refresh and show available controllers
bind - bind to a controller
stop - shutdown whole process
load - load configuration from save file
save - save configuration to save file
```

## What do I need to do to my controllers?
Print out two of the markers in the `markers` directory place them horizontally on your controller in a place the camera can see

## Why is there no Windows/Mac?
I haven't had the time to write bindings for Windows/Mac.

If you would like to write them ensure that it contains all the methods detailed in `controller.pyi`.
Then add the correct import check in `main.py`.

## Licence
The main licence is in `licence`

Note: there is code in `otherLicences` that does not fall under the same licence as the rest of this project
