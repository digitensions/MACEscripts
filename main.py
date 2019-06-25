#Coded by James Wingate for Media Archive for Central England

import os
import sys
import ffmpeg
from ffmpeg import probe
from ffprobe3 import FFProbe

aspects = [[720,  "4:3",  "SD"],
          [1280, "16:9",  "HD"],
          [1920, "16:9", "FHD"],
          [1440,  "4:3", "CHD"]]
'''
Aspects is a list of the potential aspect ratios that this script can handle
Includes ratios called in confirmation of FFprobe stream request
Gives shortform name to each file potential to correspond with .png watermark file
'''
def main():
        if len(sys.argv) >= 2:
                path = sys.argv[1]
                if (os.path.isfile(path)):
                        while True:
                                var = input("Do you want to trim this file? (y/n)\n")
                                if not (var == "y" or var == "n"):
                                        print("Invalid input, please enter either 'y' or 'n'.")
                                else:
                                        break
                                
                        if var == "n":
                                aspectRatio, resolution = getARandRes(path)
                                watermark = ffmpeg.input(getWatermark(aspectRatio))

                                (
                                        ffmpeg
                                        .input(sys.argv[1])
                                        .filter('setdar', getDAR(aspectRatio))
                                        .overlay(watermark)
                                        .output('test.mp4')
                                        .run()
                                )
                        elif var == "y":
                                start = input("Please specify the trim in point. (hh:mm:ss.mls 00:00:00.000)")
                                


                else:
                        print("ERROR: Path not valid.")

                        [1, 2, 3, 4, 5]
                        [2, 4, 6, 8, 10]

def parseTime(timeString):
        

def getDAR(aspectRatio):
        vals = [int(val) for val in aspectRatio.split(':')]
        return vals[0] / vals[1]

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

def getWatermark(ratio):
        for aspect in aspects:
                if aspect[1] == ratio:
                        standard = aspect[2]

        pngname = "{0}.png".format(standard)
        pngpath = os.path.join(os.getcwd(), "watermarks", pngname)
        return pngpath

if __name__ == '__main__':
        main()