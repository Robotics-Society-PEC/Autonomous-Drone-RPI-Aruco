# Autonomus Drone RPI

## Setting up the virtual environment

> Note : It is recommended to setup a virtual environment and then run the program
```bash
py -m venv ./venv  #creating virtual environment
venv\Scripts\activate  #to activate the environment after creation
```

## Installation and getting started

To install all the neccessary requirements run the following commands

```bash
pip install -r requirements.txt # for installation of libraries
```

## For running the program

Run the main.py file using

```bash
python main.py
```

## To Exclude files from github

To exclude files from github just add their path to the `.gitignore` file

## Adding new libraries to requirements file

To add more libraries to the `requiremnts.txt` file just install the library using pip/conda and then execute the following command in terminal

```bash
pip freeze > requirements.txt
```
## To upgrade a package already installed

```bash
pip install --upgrade --force-reinstall <package_name>
```

> Note : Apart from the PIP commands you also have to install some packages via sudo apt using the command mentioned below. This is valid for Raspberry pi.

```bash
 sudo apt install libcblas-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev 
 ```

## Important Points to note
- The failsafe inside teensy is disabled
- Do not plugin arduino nano to the USB without desoldering the wire


## Tasks

- [X] get altitude from Raspberry pi to teensy(i2c)(needs to be used)
- [X] PID for throttle using Altitude
- [X] get altitude from BMP 280
- [X] write code for mux(currenlty in altitude hold mode the pitch yaw and roll is manual)
- [X] GPS (optional)
- [X] SD Card Log Support (optional)
- [ ] Electromagnet Test
- [X] multi Aruco Support
- [ ] Landing test
- [ ] Searching algorithm in main code
- [ ] Calibration of mag needs to be done
- [X] Fix Altitude Problems (Altitude shouldn't go negative)
- [ ] Add low pass filter
- [ ] Change arming sequence according to teensy 4.1
- [ ] i2c communciation between rpi and teensy 4.1
- [ ] Throttle build up way to slow (need to increase)
- [X] Need to reduce the percentage error on the throttle build up
- [ ] Need to add limit switch
- [ ] check roll, pitch pid with I as focus
- [ ] rpi aruco fit
- [ ] throttle cap increase
- [ ] error calculation
## Our Teams Members

- Mansi Kalra
- Reeshav Chowdhury
- Soumil Arora
- Shashank Agarwal
- Rishab Sood
- Ansh Chawla
- Aayush Singla
- Vinayak Pandey

## Addresses of diffrent devices

- Teensy 0x44
- MPU6060 - 0x68
- BMP280 - 0x77
- Compass - 0x1E
- Ultrasonic - 0x20
