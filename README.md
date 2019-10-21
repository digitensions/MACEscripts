# MACEscripts

Media Archive for Central England (MACE) generated python scripts

This repository contains python3 script(s) made collaboratively between James Wingate doctoral researcher in Computer Science at University of Lincoln and Joanna White of MACE, with excellent assistance from Katherine Frances.  Wherever possible these will be heavily notated to help MACE's python skill development, and for any individuals wishing to read or test them. Please note these are TRAINING SCRIPTS and require further development and testing.  The scripts are intended to fulfil AV preservation needs though, based on MACE workflows.

We hope to add more in the future and welcome any comments, feedback and collaboration.

# Project setup

Dependencies:
* [Python 3.7](https://www.python.org/downloads/)
* [Pipenv](https://github.com/pypa/pipenv)
  - used to manage dependencies and the virtual environment

Set up the project by running:

```bash
pipenv install
```

# mp4_generator.py

This script has been developed to trim a intraframe file, deinterlace, overlay a watermark for quick distribution to clients. It has metadata additions, which can be easily edited depending upon need.

It accepts the four archival audiovisual file dimensions kept at MACE:
* SD 720x576
* HD 1280x720
* Full HD 1920x1080
* Cropped HD 1440x1080.

The `.png` watermarks are the same dimensions as the video files, with no interlacing. MACE currently is testing with a MACE logo, centralised and set at 20% opacity; the generic watermark files stored in `/watermarks` simply feature a copyright symbol for test purposes.

## Use

To run the script call:
```bash
pipenv run python mp4_generator.py /path/to/file/input.mov
```

The script will ask:
```
Where would you like the output saved?
e.g. 'home/Dave/Desktop/output.mp4'
Providing only a filename - e.g. 'file.mp4' - will export to the directory the script is in.

Do you want to deinterlace this file? ('y'/'n')
Do you want a watermark overlay on the output video? ('y'/'n')
Do you want to trim this file? ('y'/'n')

# If being trimmed:
Please specify the trim 'in' point. (hh:mm:ss.mls 00:00:00.000)
Please specify the trim 'out' point. (hh:mm:ss.mls 00:00:00.000)
```

### ⚠️ Warning ⚠️

There may be inaccuracies experienced with the trim function in FFmpeg, caused by the in/out points skipping forward or backward to the nearest keyframe if using an interframe input file (or a lossy file without gop set to 1). Please be mindful of this if you intend to use this code for archival MP4 production. It's always best to work with intraframe codecs such as Uncompressed, FFV1, ProRes etc.

# main_new.py

A variation on mp4_generator.py that first tested FFmpeg using subprocess calls. These have since been incorporated into main.py, and this script is redundant.

# name_change.py

This code searches within named columns in an excel (xlsx or csv) file, then changes existing filename from Column 2 to Column 1. It was written to help with batch filename changes. It creates a variable that focuses on two (or more) column names for the search. It uses a for loop to work through the rows within the column that end with .mov. It uses pandas to match files to a row, extract the contents of the first column then changes all ':' to '.'. The script then uses `os.rename` to change the filename to the entry in Column 1.

You would run this by first changing the code so your paths are correct (I might update this to take inputs in future), then run the command as:
```bash
pipenv run python name_change.py
```
