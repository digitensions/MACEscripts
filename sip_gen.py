# Unfinished script by James Wingate / Work in progress

import os
import sys
from uuid import uuid4
from hashlib import md5
from shutil import copy2
from datetime import datetime
from pymediainfo import MediaInfo

USERS = { '0': "Guest",
          '1': "Richard",
          '2': "Phil",
          '3': "Sue",
          '4': "Kayla",
          '5': "Eliza",
          '6': "Joanna",
          '7': "Alex" }

SUBFOLDERS = [ "objects",
               "metadata",
               "logs" ]

INVALIDCHARS = [ "\\",
                 "/",
                 ":",
                 "*",
                 "?",
                 "\"",
                 "<",
                 ">"
                 "|" ]

def main():
    try:
        while True:
            for user in USERS:
                print("[{0}]: {1}".format(user, USERS[user]))

            user_id = input("Who are you? (input the ID)\n")

            if user_id in USERS:
                print('Hi {0}.\n'.format(USERS[user_id]))
                break

        while True:
            drive_initial = input('Please enter the intake drive letter (e.g. \'D\' or \'E\'):\n')
            if check_initial(drive_initial):
                drive_initial += ':'
                break

        while True:
            img_seq = input('Do you need to process any image sequences? (y/n)\n')
            if img_seq == 'y':
                seq_dirs = handle_seq_dirs()
                print(get_seq_output(len(seq_dirs)))
            elif img_seq == 'n':
                break
            else:
                print('Please enter either \'y\', or \'n\'.\n')

        while True:
            output_path = input('Please enter the output root path\n')
            if os.path.isdir(output_path):
                print("Valid path submitted, continuing...")
                break
            else:
                print("That path was invalid!")

        while True:
            job_name = input('Please enter a unique job name\n')
            if (
                1 not in [c in job_name for c in INVALIDCHARS]
                and len(job_name) >= 2
            ):
                if not os.path.exists(os.path.join(output_path, job_name)):
                    os.mkdir(os.path.join(output_path, job_name))
                    break
                else:
                    reuse_job = reuse_job_name()
                    if reuse_job:
                        break
            else:
                print("That job name contains invalid characters.")
    except:
        sys.exit("One (or more) of your inputs was incorrect, please re-run try again.")

    files_valid, files_invalid = [0 for _ in range(2)]

    for file in os.listdir(drive_initial):
        if not file.startswith('.'):
            try:
                file_path = os.path.join(drive_initial, file)
                media_info = MediaInfo.parse(file_path)
                if check_valid(media_info):
                    files_valid += 1
                    print('{0} \'{1}\' is valid, reading...'.format(gen_prefix(), file))

                    # Create UUID base folder.
                    item_uuid = gen_uuid()
                    os.mkdir(os.path.join(output_path, job_name, item_uuid))

                    for dirname in SUBFOLDERS:
                        os.mkdir(os.path.join(output_path, job_name, item_uuid, dirname))
                        if dirname == 'objects':
                            safe_copy(file_path, os.path.join(output_path, job_name, item_uuid, dirname), file)

                else:
                    files_invalid += 1
                    print('{0} \'{1}\' is invalid, skipping...'.format(gen_prefix(), file))
            except:
                print('{0} \'{1}\' could not be read, skipping...'.format(gen_prefix(), file))

def safe_copy(src, dst, filename):
    while True:
        md5_orig = gen_md5(src)
        copy2(src, os.path.join(dst, filename))
        md5_after = gen_md5(os.path.join(dst, filename))

        print(md5_orig == md5_after)
        if md5_orig == md5_after:
            with open(os.path.join(dst, filename + '_checksum.md5'), 'w') as writer:
                writer.write(md5_after)
            break
        else:
            os.delete(os.path.join(dst, filename))
            print('Checksums did not match, trying again...')


def reuse_job_name():
    while True:
        reuse_name = input("That job name already exists\n\
        Would you like to add to it (y), or define a new one? (n)")
        if reuse_name == 'y':
            return True
        elif reuse_name == 'n':
            return False
        else:
            print("Input must be either 'y' or 'n'.")

def handle_seq_dirs():
    seq_paths = []
    while True:
        seq_dir = input('Please specify an image sequence directory\ne.g. path/to/image_directory\n(or \'n\' if you are done)\n').strip('\"')
        if seq_dir != 'n':
            if os.path.isdir(seq_dir):
                seq_paths.append(seq_dir)
                print('Input was a valid directory, saving...\n')
            else:
                print('Input was not a valid directory.\n')
        else:
            return seq_paths

def get_seq_output(seq_num):
    if seq_num > 0:
        if seq_num == 1:
            return ('{0} image sequence submitted. Continuing...\n'.format(seq_num))
        else:
            return ('{0} image sequences submitted. Continuing...\n'.format(seq_num))
    else:
        return ('No image sequences submitted. Continuing...\n')

def check_initial(initial):
    if len(initial) == 1 and os.path.isdir(initial + ':'):
        return True
    else:
        print('Drive does not exist.\n')
        return False

def check_valid(media_info):
    return any(
        track.track_type in ['Video', 'Audio'] for track in media_info.tracks
    )

def gen_prefix():
    return '[{0}]'.format(str(datetime.now().time().strftime("%H:%M:%S")))

def gen_md5(file):
    hash = md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

def gen_uuid():
    return str(uuid4())

if __name__ == '__main__':
    main()
