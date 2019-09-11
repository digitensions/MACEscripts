# Coded by James Wingate, Katherine Frances Nagels and Joanna White

from ffprobe3 import FFProbe
import os
import re
import subprocess
import sys

# The keys are the shortform name for each resolution,
# corresponding to the expected .png watermark file.
# .png files are sized the same as SD, HD, Full HD and cropped HD (1440x1080) video
RESOLUTIONS = {
    "SD": {
        "aspect_ratio": "4:3",
        "width":         720,
        "full_name":    "Standard definition"
    },
    "HD": {
        "aspect_ratio": "16:9",
        "width":         1280,
        "full_name":    "High definition"
    },
    "FHD": {
        "aspect_ratio": "16:9",
        "width":         1920,
        "full_name":    "Full high definition"
    },
    "CHD": {
        "aspect_ratio": "4:3",
        "width":         1440,
        "full_name":    "Cropped high definition"
    },
}


# Main function, script entrypoint.
def main():
    # In regards to 'argument', it refers to each value after 'python'/'python3':
    # e.g. 'python main.py home/example/video.mp4'
    # In the above example, 'main.py' is argument 0, and the path is argument 1.
    # This is because all indexing in programming languages starts at 0.

    if len(sys.argv) < 2:
        print("Please call the script with the path to a video file!\n"
              "e.g. python3 main.py path/to/video.mov")

    # If the script has been called with two or more arguments
    else:
        # Set the input_file variable to the 2nd argument (input file path).
        input_file = sys.argv[1]

        if not (os.path.isfile(input_file)):
            print("ERROR: Path not valid.")

        # If the path is a legitimate file...
        else:
            ffmpeg_command = create_ffmpeg_command(input_file)

            print("Transcoding with:", " ".join(ffmpeg_command), "\n")

            subprocess.call(ffmpeg_command)


def create_ffmpeg_command(input_file):
    output_path = set_output_path(input_file)

    to_watermark = set_watermark_status()
    to_trim = set_trim_status()

    aspect_ratio = stream_aspect_ratio(input_file)
    dar = display_aspect_ratio(aspect_ratio)
    watermark_file = watermark_path(aspect_ratio)

    ffmpeg_program_call = [
        "ffmpeg"
    ]

    input_video_file = [
        "-i", input_file
    ]

    watermark_settings = [
        "-i", watermark_file,
        "-filter_complex", "overlay"  # overlay filter for supplied png
    ]

    stream_settings = [
        # TODO "setdar=dar={0}".format(dar),   # set DAR to aspect ratio
        "-c:v",     "libx264",          # encode video stream as H.264
        "-pix_fmt", "yuv420p",          # 4:2:0 chroma subsubsampling
        "-c:a",     "aac",              # encode audio stream(s) as AAC
        "-map",     "0",       "-dn"    # map all streams except data streams to output
    ]

    output_settings = [
        "-metadata", "copyright=Media Archive for Central England",
        "-metadata", "comment=Please contact MACE to license this footage on 01522 837750",
        output_path,
        "-report"     # Generates log in current directory
    ]

    if not to_trim:
        if to_watermark:
            return ffmpeg_program_call + input_video_file + watermark_settings + stream_settings + output_settings
        else:
            return ffmpeg_program_call + input_video_file + stream_settings + output_settings

    # If the user selects to trim...
    elif to_trim:
        # Get the start and end trim in points from the user.
        in_point = set_timestamp(
            "Please specify the trim 'in' point")
        out_point = set_timestamp(
            "Please specify the trim 'out' point")

        trim_settings = [
            "-ss", in_point,
            "-to", out_point
        ]

        if to_watermark:
            return ffmpeg_program_call + trim_settings + input_video_file + watermark_settings + stream_settings + output_settings
        else:
            return ffmpeg_program_call + trim_settings + input_video_file + stream_settings + output_settings


def display_aspect_ratio(ratio_string):
    # Get the numeric ratio from the aspect ratio string, e.g. "4:3" → 1.333(3)

    numbers = ratio_string.split(":")
    width = int(numbers[0])
    height = int(numbers[1])

    return width / height


def stream_aspect_ratio(file):
    # Returns the aspect ratio expressed as a string, e.g. "4:3"

    file_metadata = FFProbe(file)
    ratio = None

    for stream in file_metadata.streams:
        if stream.is_video():
            width, height = stream.frame_size()

            for resolution in RESOLUTIONS:
                if RESOLUTIONS[resolution]["width"] == width:
                    ratio = RESOLUTIONS[resolution]["aspect_ratio"]
                    return ratio

    if not ratio:
        print("Incompatible input dimensions.")
        sys.exit()


def watermark_path(ratio):
    # Function to get a path to a corresponding .png watermark given an aspect ratio string.

    for name, _ in RESOLUTIONS.items():
        if RESOLUTIONS[name]["aspect_ratio"] == ratio:
            standard = name  # sets standard to "HD", "SD", etc

    file_name = "{0}.png".format(standard)
    file_path = os.path.join(os.getcwd(), "watermarks", file_name)
    return file_path


def set_output_path(input_path):
    output_path = input("Where would you like the output saved?\n"
                        "e.g. 'home/Dave/Desktop/output.mp4'\n"
                        "Providing only a filename - e.g. 'file.mp4' - will export to the directory the script is in.\n")

    if output_path:
        return output_path

    else:
        filename, extension = os.path.splitext(input_path)
        default_output_path = "{0}_access_copy{1}".format(filename, extension)

        print("No output file path given!\n"
              "Saving as default: {0}".format(default_output_path))

        return default_output_path


def set_trim_status():
    trim = input("Do you want to trim this file? ('y'/'n')\n")

    if not (trim == "y" or trim == "n"):
        print("Invalid input! I'll ask again")
        set_trim_status()
    else:
        return trim == "y"


def set_watermark_status():
    use_watermark = input(
        "Do you want a watermark overlay on the output video? ('y'/'n')\n")

    if not (use_watermark == "y" or use_watermark == "n"):
        print("Invalid input! I'll ask again")
        set_watermark_status()
    else:
        return use_watermark == "y"


def set_timestamp(message):
    timestamp = input("{0}. (hh:mm:ss.mls 00:00:00.000)\n".format(message))

    if valid_timestamp(timestamp):
        return timestamp
    else:
        print("Invalid timestamp!\n"
              "It must be in the format hh:mm:ss.mls (00:00:00.000).")
        try_again = input("Try again? ('y'/'n')\n")
        if try_again == 'y':
            set_timestamp(message)
        else:
            print("Exiting!")
            sys.exit()


def valid_timestamp(timestamp):
    TIMESTAMP_REGEX = re.compile("\d{2}:\d{2}:\d{2}.\d{3}") # Matches the pattern 00:00:00.000 (hh:mm:ss.mls)
    match = re.search(TIMESTAMP_REGEX, timestamp)
    return bool(match)


# Run the main function as entrypoint.
if __name__ == "__main__":
    main()
