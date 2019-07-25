#Coded by James Wingate for Media Archive for Central England

import os
import sys
import ffmpeg
from ffmpeg import probe
from ffprobe3 import FFProbe
import re

# Array of arrays with each internal array representing an expected input resolution.
# Includes ratios called in confirmation of FFprobe stream request.
# Gives shortform name for each expected corresponding .png watermark file.
# .png files are sized the same as SD, HD, Full HD and cropped HD (1440x1080) video
RESOLUTIONS = [[720,  "4:3",  "SD"],
              [1280, "16:9",  "HD"],
              [1920, "16:9", "FHD"],
              [1440,  "4:3", "CHD"]]

# Main function, script entrypoint.
def main():
        # In regards to 'argument', it refers to each value after 'python'/'python3':
        # e.g. 'python main.py home/example/video.mp4'
        # In the above example, 'main.py' is argument 0, and the path is argument 1.
        # This is because all indexing in programming languages starts at 0.

        if len(sys.argv) < 2:
            print('Please call the script with the path to a video file!\n'
                  'e.g. python3 main.py path/to/video.mkv')

        # If the script has been called with two or more arguments
        else:
                # Set the input_file variable to the 2nd argument (input file path).
                input_file = sys.argv[1]

                # If the path is a legitimate file...
                if (os.path.isfile(input_file)):
                        # Loop until break is called.
                        while True:
                                # Obtain user input.
                                to_trim = input("Do you want to trim this file? (y/n)\n")
                                if not (to_trim == "y" or to_trim == "n"):
                                        print("Invalid input, please enter either 'y' or 'n'.")
                                else:
                                        break
                                
                        # Get aspect ratio, resolution, and watermark image.
                        aspect_ratio, resolution = aspect_ratio_and_resolution(input_file)
                        watermark = ffmpeg.input(watermark_path(aspect_ratio))

                        # Ask user for their preferred output filename/filepath.
                        output_path = input("Where would you like the output saved?\n"
                                        "e.g. 'home/Dave/Desktop/output.mp4'\n"
                                        "Providing only a filename will export to the directory the script is in.\n"
                                        "e.g. 'file.mp4' with no path.\n")

                        while True:
                                # Obtain user input.
                                watermark = input("Do you want a watermark overlay on the output video? (y/n)")
                                if not (watermark == "y" or watermark == "n"):
                                        print("Invalid input, please enter either 'y' or 'n'.")
                                else:
                                        break

                        # If the user selects to not trim...
                        if to_trim == "n":
                                if watermark == "y":
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(input_file)
                                                .filter('setdar', display_aspect_ratio(aspect_ratio))
                                                .overlay(watermark)
                                                .output(output_path)
                                                .run()
                                        )
                                else:
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(input_file)
                                                .filter('setdar', display_aspect_ratio(aspect_ratio))
                                                .output(output_path, vcodec = "libx264", pix_fmt = "yuv420p", acodec = "aac", crf = "23")
                                                .run()
                                        )

                        # If the user selects to trim...
                        elif to_trim == "y":
                                # Get the start and end trim in points from the user.
                                in_point = collect_timestamp("Please specify the trim 'in' point")
                                out_point = collect_timestamp("Please specify the trim 'out' point")

                                if watermark == "y":
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(input_file)
                                                .trim(start = in_point, end = out_point)
                                                .overlay(watermark)
                                                .output(output_path, vcodec = "libx264", pix_fmt = "yuv420p", acodec = "aac", crf = "23")
                                                .run()
                                        )
                                else:
                                        # Make the ffmpeg call.
                                        (
                                                ffmpeg
                                                .input(input_file)
                                                .trim(start = in_point, end = out_point)
                                                .output(output_path, vcodec = "libx264", pix_fmt = "yuv420p", acodec = "aac", crf = "23")
                                                .run()
                                        )
                else:
                        print("ERROR: Path not valid.")

# Function to get the DAR from a given aspect ratio string.
def display_aspect_ratio(string):
        vals = [int(val) for val in string.split(':')]
        return vals[0] / vals[1]

# Function to get the aspect ratio and resolution from a given path to a video.
def aspect_ratio_and_resolution(file):
        file_metadata = FFProbe(file)

        for stream in file_metadata.streams:
                if stream.is_video():
                        width, height = stream.frame_size()
                        
                        ratio = ""
                        for resolution in RESOLUTIONS:
                                if resolution[0] == width:
                                        ratio = resolution[1]
                                        break

                        if ratio == "":
                                print("Incompatible input dimensions.")
                                sys.exit()
                        
        return ratio, [width, height]

# Function to get a path to a corresponding .png watermark given an aspect ratio string.
def watermark_path(ratio):
        for resolution in RESOLUTIONS:
                if resolution[1] == ratio:
                        standard = resolution[2]

        file_name = "{0}.png".format(standard)
        file_path = os.path.join(os.getcwd(), "watermarks", file_name)
        return file_path


def collect_timestamp(message):
    timestamp = input("{0}. (hh:mm:ss.mls 00:00:00.000)\n".format(message))

    if valid_timestamp(timestamp):
        return timestamp
    else:
        print("Invalid timestamp! \nIt must be in the format hh:mm:ss.mls (00:00:00.000).")
        try_again = input("Try again? ('y'/'n')")
        if try_again == 'y':
            collect_timestamp(message)
        else:
            print('Exiting!')
            sys.exit()


def valid_timestamp(timestamp):
    TIMESTAMP_REGEX = re.compile('\d{2}:\d{2}:\d{2}.\d{3}') # Matches the pattern 00:00:00.000 (hh:mm:ss.mls)
    match = re.search(TIMESTAMP_REGEX, timestamp)
    return bool(match)


# Run the main function as entrypoint.
if __name__ == '__main__':
        main()
