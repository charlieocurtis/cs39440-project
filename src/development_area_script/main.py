from PIL import Image
from sklearn.metrics import mean_squared_error

import numpy as np
import pandas as pd
import sample_images.image_init as sample

PNG_FILE = "test_image.png"
BMP_FILE = "test_image.bmp"
JPG_FILE = "test_image.jpg"
BMP_PIX_WRITE = "output.txt"
LUMINANCE_WRITE = "luminance-out.txt"
LUMINANCE_DF = pd.DataFrame()


def png_to_bmp(input_file, output_file):
    # collect the png file
    image = Image.open(input_file)

    # save the png into bmp
    image.save(output_file)


def png_to_jpg():
    # collect a sample image to convert rto jpg
    image = sample.LWAC01_PNG
    # solution for a workaround of a bug found at: https://stackoverflow.com/a/7248480
    image.mode = 'I'
    image.point(lambda i:i*(1./256)).convert('L').save(sample.LWAC01_JPG)


def collect_bmp_pixel_vals(image_to_open):
    # collect each pixel rgb values and put into np array
    # in the case of png image this also contains alpha field
    bmp_pix_vals = np.asarray(Image.open(image_to_open).getdata())
    return bmp_pix_vals


def collect_luminance_vals(image_to_open: Image):
    # converts image to grey scale and then collects luminance values
    # conversion method in docs
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


def calculate_mse(reference_image, subject_image):
    # placing the luminance values for both images into pandas dataframes
    # since can be used in mean_squared_error function
    luminance_bmp_df = pd.DataFrame(collect_luminance_vals(subject_image))
    luminance_png_df = pd.DataFrame(collect_luminance_vals(reference_image))
    return mean_squared_error(luminance_png_df, luminance_bmp_df)


def main():
    # png_to_bmp(PNG_FILE, BMP_FILE)
    # collect_bmp_pixel_vals(BMP_FILE)
    # collect_bmp_luminance_vals(BMP_FILE)
    # print(calculate_mse())
    # png_to_jpg(sample.LWAC01_PNG, sample.LWAC01_JPG)
    print(calculate_mse("sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png", "LWAC01_JPG.jpg"))

    # looking for physical pixel differences between png/bmp variant and jpg variant
    # since jpg has known compression algorithm good image type for testing
    # png variant was put through online conversion at: https://www.freeconvert.com/
    # mse for png and jpg variants = 1.0559869541551807

    # write_bmp_pixel_vals(BMP_PIX_WRITE, collect_bmp_pixel_vals(BMP_FILE))
    # write_bmp_pixel_vals("jpg-output.txt", collect_bmp_pixel_vals(JPG_FILE))


if __name__ == "__main__":
    main()
