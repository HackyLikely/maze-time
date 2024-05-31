#!/usr/bin/python3

import os
import sys
import imageio.v2 as imageio




def create_gif_from_images(directory, output_file, fps=12):

    # Get a list of all PNG files in the directory
    image_files = sorted([file for file in os.listdir(directory) if file.endswith('.png')])

    # Iterate through each image file, add it to the images list
    images = []
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        images.append(imageio.imread(image_path))

    # Write GIF file
    duration = 1/fps
    imageio.mimsave(output_file, images, duration=duration, loop=0)



# get argument
directory = sys.argv[1]

# Check if the directory ends with "/"
if directory.endswith("/"):
    # Remove the trailing "/"
    directory = directory[:-1]

output_file = f'{directory}.gif'
fps = 8
create_gif_from_images(directory, output_file, fps)