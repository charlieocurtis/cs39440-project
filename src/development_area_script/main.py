from PIL import Image, ImageOps
from sklearn.metrics import mean_squared_error

import sys
import numpy as np
import pandas as pd
import sample_images.image_init as sample

np.set_printoptions(threshold=sys.maxsize)

PNG_FILE = "test_image.png"
BMP_FILE = "test_image.bmp"
JPG_FILE = "test_image.jpg"
BMP_PIX_WRITE = "output.txt"
LUMINANCE_WRITE = "luminance-out.txt"
LUMINANCE_DF = pd.DataFrame()
DIFFERENCE_DATAFRAME = pd.DataFrame()


def png_to_bmp(input_file, output_file):
    # collect the png file
    image = Image.open(input_file)

    # save the png into bmp
    image.mode = 'I'
    image.point(lambda i: i * (1. / 256)).convert('L').save("LWAC01.bmp")


def png_to_jpg():
    # collect a sample image to convert to jpg
    image = sample.LWAC03_PNG
    # solution for a workaround of a bug found at: https://stackoverflow.com/a/7248480
    image.mode = 'I'
    image.point(lambda i: i * (1. / 256)).convert('L').save(sample.LWAC03_JPG)


def jpg_to_png():
    image = Image.open("LWAC01_JPG.jpg")
    image.save("LWAC01_JPG_to_PNG.png", format="png")


def collect_bmp_pixel_vals():
    # collect each pixel rgb values and put into np array
    # in the case of png image this also contains alpha field
    bmp_pix_vals = np.asarray(Image.open("sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png").getdata())
    return bmp_pix_vals


def collect_luminance_vals_8bit(target_image):
    # converts image to grey scale and then collects luminance values
    # conversion method in docs
    luminance = np.asarray(Image.open(target_image).convert("L"))
    return luminance


def collect_luminance_vals_16bit(target_image):
    # conversion argument different for 16 bit AUPE images
    luminance = np.asarray(Image.open(target_image).convert("I;16"))
    return luminance


def write_bmp_pixel_vals(filename, pixel_vals):
    # mainly used for debugging
    # write each tuple to the output file ready to be read and compared with original
    with open(filename, "w") as file:
        for rgb in pixel_vals:
            file.write(str(rgb)[1:-1])
            file.write("\n")


def write_luminance_vals(filename, luminance_vals):
    # counter is for debugging purposes when trying to establish
    # how the library is outputting data into the given text file
    # counter = 0
    with open(filename, "w") as file:
        for line in luminance_vals:
            file.write(str(line))
            file.write("\n")
            # counter += 1


def calculate_mse(reference_image, subject_image):
    # placing the luminance values for both images into pandas dataframes
    # since can be used in mean_squared_error function
    luminance_bmp_df = pd.DataFrame(collect_luminance_vals_8bit(subject_image))
    luminance_png_df = pd.DataFrame(collect_luminance_vals_8bit(reference_image))
    return mean_squared_error(luminance_png_df, luminance_bmp_df)


def calculate_difference(image_one, image_two):
    # load first image
    image_one_values = pd.DataFrame(collect_luminance_vals_8bit(image_one))

    # write pixel vals to file for debugging
    # with open("image-one-output.txt", "w") as file:
    #     file.write(str(image_one_values))

    # load second image
    image_two_values = pd.DataFrame(collect_luminance_vals_16bit(image_two))
    # convert from 16bit to 8bit
    image_two_values = (image_two_values * 1.) / 256

    # with open("image-two-output.txt", "w") as file:
    #     file.write(str(image_two_values))

    # return the absolute difference between the two images
    resultant = pd.DataFrame(image_two_values - image_one_values)

    return resultant


def find_mode(target_image):
    # find the current mode of the required image
    image = Image.open(target_image)
    print(image.mode)


def main():
    created_image = Image.fromarray(np.asarray(calculate_difference("test_image.png",
                                                        "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png")))
    created_image.show()


if __name__ == '__main__':
    main()
