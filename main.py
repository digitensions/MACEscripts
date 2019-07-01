#Coded by James Wingate for Media Archive for Central England

import os
import sys
import ffmpeg
from ffmpeg import probe
from ffprobe3 import FFProbe

# Array of arrays with each internal array representing an expected input resolution.
# Includes ratios called in confirmation of FFprobe stream request.
# Gives shortform name for each expected corresponding .png watermark file.
aspects = [[720,  "4:3",  "SD"],
          [1280, "16:9",  "HD"],
          [1920, "16:9", "FHD"],
          [1440,  "4:3", "CHD"]]

# Main function, script entrypoint.
def main():
        # In regards to 'argument', it refers to each value after 'python'/'python3':
        # e.g. 'python main.py home/example/video.mpeg'
        # In the above example, 'main.py' is argument 0, and the path is argument 1.
        # This is because all indexing in programming languages starts at 0.

        # If the number of arguments passed is greater than or equal to 2...
        if len(sys.argv) >= 2:
                # Set the path variable to the 2nd argument (path).
                path = sys.argv[1]

                # If the path is a legitimate file...
                if (os.path.isfile(path)):
                        # Loop until break is called.
                        while True:
                                # Obtain user input.
                                var = input("Do you want to trim this file? (y/n)\n")
                                if not (var == "y" or var == "n"):
                                        print("Invalid input, please enter either 'y' or 'n'.")
                                else:
                                        break
                                
                        # Get aspect ratio, resolution, and watermark image.
                        aspectRatio, resolution = getARandRes(path)
                        watermark = ffmpeg.input(getWatermark(aspectRatio))

                        # Ask user for their preferred output filename/filepath.
                        outpath = input("Where would you like the output saved?\n"
                                        "e.g. 'home/Dave/Desktop/output.mpeg'\n"
                                        "Providing only a filename will export to the directory the script is in.\n"
                                        "e.g. 'file.mpeg' with no path.\n")

                        while True:
                                # Obtain user input.
                                wtrmrk = input("Do you want a watermark overlay on the output video? (y/n)")
                                if not (wtrmrk == "y" or wtrmrk == "n"):
                                        print("Invalid input, please enter either 'y' or 'n'.")
                                else:
                                        break

                        # If the user selects to not trim...
                        if var == "n":
                                if wtrmrk == "y":
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(sys.argv[1])
                                                .filter('setdar', getDAR(aspectRatio))
                                                .overlay(watermark)
                                                .output(outpath)
                                                .run()
                                        )
                                else:
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(sys.argv[1])
                                                .filter('setdar', getDAR(aspectRatio))
                                                .output(outpath, vcodec = "libx264", acodec = "aac")
                                                .run()
                                        )

                        # If the user selects to trim...
                        elif var == "y":
                                # Get the start and end trim in points from the user.
                                trimstart = input("Please specify the trim in point. (hh:mm:ss.mls 00:00:00.000)\n")
                                trimend = input("Please specify the trim out point. (hh:mm:ss.mls 00:00:00.000)\n")
                                
                                if wtrmrk == "y":
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(sys.argv[1])
                                                .trim(start = trimstart, end = trimend)
                                                .overlay(watermark)
                                                .output(outpath, vcodec = "libx264", acodec = "aac")
                                                .run()
                                        )
                                else:
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(sys.argv[1])
                                                .trim(start = trimstart, end = trimend)
                                                .output(outpath, vcodec = "libx264", acodec = "aac")
                                                .run()
                                        )
                else:
                        print("ERROR: Path not valid.")

# Function to parse the trim time from the given string.
def parseTime(timeString):
        # Splits input time into format [hours, minutes, [seconds, milliseconds]].
        return [val.split('.') for val in timeString.split(':')]

# Function to get the DAR from a given aspect ratio string.
def getDAR(aspectRatio):
        vals = [int(val) for val in aspectRatio.split(':')]
        return vals[0] / vals[1]

# Function to get the aspect ratio and resolution from a given path to a video.
def getARandRes(path):
        inputfile = FFProbe(path)

        for stream in inputfile.streams:
                if stream.is_video():
                        width, height = stream.frame_size()
                        
                        ratio = ""
                        for aspect in aspects:
                                if aspect[0] == width:
                                        ratio = aspect[1]
                                        break

                        if ratio == "":
                                print("Incompatible input dimensions.")
                                sys.exit()
                        
        return ratio, [width, height]

# Function to get a path to a corresponding .png watermark given an aspect ratio string.
def getWatermark(ratio):
        for aspect in aspects:
                if aspect[1] == ratio:
                        standard = aspect[2]

        pngname = "{0}.png".format(standard)
        pngpath = os.path.join(os.getcwd(), "watermarks", pngname)
        return pngpath

# Run the main function as entrypoint.
if __name__ == '__main__':
        main()
