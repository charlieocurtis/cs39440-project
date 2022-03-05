import pandas
from PIL import Image

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

PNG_FILE = "test_image.png"
BMP_FILE = "test_image.bmp"
JPG_FILE = "test_image.jpg"
BMP_PIX_WRITE = "output.txt"
LUMINANCE_WRITE = "luminance-out.txt"
LUMINANCE_DF = pandas.DataFrame()


def png_to_bmp(input_file, output_file):
    # collect the png file
    image = Image.open(input_file)

    # convert the png into bmp
    image.save(output_file)


def collect_bmp_pixel_vals(image_to_open):
    # collect each pixel rgb values and put into list
    # in the case of png image this also contains alpha field
    bmp_pix_vals = list(Image.open(image_to_open).getdata())
    return bmp_pix_vals


def collect_bmp_luminance_vals(image_to_open: Image):
    # converts image to grey scale and then collects luminance values
    # can now calculate MSE
    luminance = np.asarray(Image.open(image_to_open).convert("L"))
    return luminance


def collect_png_luminance_vals(image_to_open: Image):
    luminance = np.asarray(Image.open(image_to_open).convert("L"))
    return luminance


def write_bmp_pixel_vals(filename, pixel_vals):
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


def calculate_mse():
    luminance_bmp_df = pandas.DataFrame(collect_bmp_luminance_vals(PNG_FILE))
    luminance_png_df = pandas.DataFrame(collect_png_luminance_vals(JPG_FILE))
    return mean_squared_error(luminance_png_df, luminance_bmp_df)


def main():
    # png_to_bmp(PNG_FILE, BMP_FILE)
    # collect_bmp_pixel_vals(BMP_FILE)
    # collect_bmp_luminance_vals(BMP_FILE)
    print(calculate_mse())

    # looking for physical pixel differences between png/bmp variant and jpg variant
    # since jpg has known compression algorithm good image type for testing
    # png variant was put through online conversion at: https://www.freeconvert.com/
    # mse for png and jpg variants = 1.0559869541551807

    # write_bmp_pixel_vals(BMP_PIX_WRITE, collect_bmp_pixel_vals(BMP_FILE))
    # write_bmp_pixel_vals("jpg-output.txt", collect_bmp_pixel_vals(JPG_FILE))


if __name__ == "__main__":
    main()
