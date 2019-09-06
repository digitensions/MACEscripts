# MACEscripts
MACE generated python codes

This repository contains python3 script(s) made collaboratively between James Wingate doctoral researcher in Computer Science at University of Lincoln, and Joanna White of the Media Archive of Central England.  Wherever possible these will be heavily notated to help MACE's python development, and for any individuals wishing to read or test them. Please note these are TRAINING SCRIPTS and require further development/testing.  The scripts are intended to meet / fulfil AV preservation needs though, based on MACE workflows.

We hope to add more in coming weeks, and for MACE to attempt codes of their own in following months. We welcome any commends, feedback and collaboration.

# main.py

This script has been developed for anyone to easily trim a file and overlay a watermark for quick/easy distribution to clients.

It accepts the four archival audiovisual file dimensions kept at MACE:
* SD 720x576
* HD 1280x720
* Full HD 1920x1080
* Cropped HD 1440x1080.

The `.png` watermarks are the same dimensions as the video files. MACE uses a MACE logo, centralised and set at 20% opacity; the generic watermark files stored in `/watermarks` simply feature a copyright symbol.

## Dependencies

* [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
* [ffprobe3](https://github.com/DheerendraRathor/ffprobe3)

## Use

To run the code call:
```bash
python3 main.py /path_to_file/input.mov
```

The script will ask:
```
Do you want to trim this file? ('y'/'n')
Do you want a watermark overlay on the output video? ('y'/'n')

Where would you like the output saved?
e.g. 'home/Dave/Desktop/output.mp4'
Providing only a filename - e.g. 'file.mp4' - will export to the directory the script is in.

# If being trimmed:
Please specify the trim 'in' point. (hh:mm:ss.mls 00:00:00.000)
Please specify the trim 'out' point. (hh:mm:ss.mls 00:00:00.000)
```

### ⚠️ Warning ⚠️

There may be inaccuracies experienced with the trim function in FFmpeg, caused by the in/out points skipping forward or backward to the nearest keyframe.  
At present I'm unsure how to resolve this issue, so please be mindful of this if you intend to use this code for actual archival MP4 production.

# main_new.py

A variation on Main.py that has removed ffmpeg-python for the FFmpeg calls and replaced with subprocess calls, that allow you to more directly dictate the way your FFmpeg command is called.  This is essential to allow the -ss call to fall before the -i on the command line.  The crop function still needs more testing as there are long gop issues with this function - have to read up more and see if there are ways of making crops more accurate.  We've only tested with input files that are ProRes 422HQ so far.

# name_change.py

This code searches within named columns in an excel (xlsx or csv) file, then changes existing filename from Column 2 to Column 1. It was written to help with batch filename changes. It creates a variable that focuses on two (or more) column names for the search. It uses a for loop to work through the rows within the column that end with .mov. It uses pandas to match files to a row, extract the contents of the first column then changes all ':' to '.'. The script then uses os.rename to change the filename to the entry in Column 1.

You would run this by first changing the code so your paths are correct (I might update this to take inputs in future), then run the command as:
```
python3 name_change.py
```
