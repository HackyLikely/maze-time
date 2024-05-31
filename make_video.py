#!/usr/bin/python3

# pip install imageio
# pip install imageio[ffmpeg]
# pip install imageio[pyav]

import os
import sys
import imageio.v2 as imageio


def create_video_from_images(directory, output_file, fps=12):

    # Get a list of all PNG files in the directory
    image_files = sorted([file for file in os.listdir(directory) if file.endswith('.png')])

    # Create a writer object to write the video
    writer = imageio.get_writer(output_file, fps=fps)

    # Iterate through each image file, add it to the video
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        image = imageio.imread(image_path)
        writer.append_data(image)

    # Close the writer
    writer.close()



# get argument
directory = sys.argv[1]

# Check if the directory ends with "/"
if directory.endswith("/"):
    # Remove the trailing "/"
    directory = directory[:-1]

output_file = f'{directory}.mp4'
fps = 8
create_video_from_images(directory, output_file, fps)