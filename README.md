# Zrecorder 

A system that joins Zoom meetings, records them with OBS Studio and
uploads the resulting file to storage services. There are two ways
that system functions.

## First way (WIP)

The first way is specific to Windows. It consists of OBS Studio
profiles for the different kinds of meetings that you would like to
record, your browser which shall be used to open / join meetings on
teleconferencing services, and a batch script that ties everything
together. 

### OBS Studio

The system uses separate OBS Studio profiles for the different types
of recordings that will be made. You may want to store the resulting
video files in separate directories according to topic or have
diferent recording settings for each category of recorded videos, for
example. To setup the system you will first need to create separate
OBS Studio profiles, from the _Profile_ menu, and then create
different Windows shortcuts with the different profile arguments. You
can append the following command line arguments to a copy of an
existing OBS Studio shortcut on the Desktop (p.ex.): 
```
--profile "OBS PROFILE NAME" --startrecording
```
The `--startrecording` instructs OBS Studio to start recording as soon
as it starts. You can place those shortcuts on the Desktop, or inside
a folder. You are not going to use them directly.

### Setting up the browser

Make sure that the browser that will be used by the batch script is
setup to open / join the meeting directly, without requiring user
input. The browser should open the relevant clients / join the meeting
when given a URL as an argument from the command line.

### Batch script

The batch script is responsible for starting the browser (in order to
start / join the meeting) and start OBS Studio from the previously
created shortcuts. The script is in `Zrec.bat`. It takes two arguments
and can be run from the command line or from a shortcut (on the
Desktop p.ex.); the first one is the path of the OBS Studio (profile
specific) shortcut from above and the second one is the URL of the
meeting. The arguments are space-separated. If any of the paths or
names contains spaces or special characters they will need to placed
inside quotes (`"`).

## Second way
