# MACEscripts
MACE generated python codes

This repository contains python3 script(s) made collaboratively between James Wingate doctoral researcher in Computer Science at University of Lincoln, and Joanna White of the Media Archive of Central England.  Wherever possible these will be heavily notated to help MACE's python development, and for any individuals wishing to read or test them. Please note these are TRAINING SCRIPTS and require further development/testing.

We hope to add more in coming weeks, and for MACE to attempt codes of their own in following months. We welcome any commends, feedback and collaboration.

# Main.py

This script has been developed for anyone to easily trim a file and overlay a watermark for quick/easy distribution to clients. It has been developed to accept the four archival audiovisual file dimensions kept at MACE: SD 720x576; HD 1280x720; Full HD 1920x1080; and Cropped HD 1440x1080.  The .png watermarks are the same dimensions as the video files, and for test purposes we use a MACE logo centralised and set at 20% opacity. These PNGs should be stored alongside the main.py script in a directory named 'watermarks'.

To run the code call:
`python3 main.py /path_to_file/input.mov`

The script will ask:
```
Do you want to trim this file? (y/n); 
Where would you like the output file saved? (drag and drop a directory before typing name_of_file.mp4); 
Do you want a watermark overlay on the output video? (y/n); 
Please specify the trim 'in' point. (hh:mm:ss.mls 00:00:00.000); 
Please specify the trim 'out' point. (hh:mm:ss.mls 00:00:00.000).
```

Then the FFmpeg encoding will begin and the .mp4 will be placed in your specified location.

External libraries are required for this script including FFmpeg-python PyPi available from: https://pypi.org/project/ffmpeg-python/

NOTE: There may be inaccuracies experienced with the trim function in FFmpeg which can be caused by the in/out points skipping forward or backward to the nearest keyframe. At present I'm unsure how to resolve this issue so please be mindful of this if you intend to use this code for actual archival MP4 production.
