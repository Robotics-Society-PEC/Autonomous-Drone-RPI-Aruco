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

## Tasks

- [] get altitude from Raspberry pi to teensy(i2c)
- [] PID for throttle using Altitude
- [X] get altitude from BMP 280
- [] write code for mux(currenlty in altitude hold mode the pitch yaw and roll is manual)

## Our Teams Members

- Mansi Kalra
- Reeshav Chowdhury
- Soumil Arora
- Shashank Aggarwal
- Rishab Sood
- Ansh Chawla
- Aayush Singla
- Vinayak Pandey
- Darren Chahal
- Kushal Nandi

Special Thanks to Yash Jindal for keeping our motivation High and Cheering us througout the process.
