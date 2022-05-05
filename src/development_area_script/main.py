from PIL import Image
from sklearn.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd

np.set_printoptions(threshold=sys.maxsize)


def find_mode(subject_image):
    """
    Find the current mode of the required image

    :param subject_image: The image that will have its mode checked
    :type subject_image: String
    :return: The PIL defined 'mode' of the image
    """
    image = Image.open(subject_image)
    return image.mode


def check_colour_depth(subject_image):
    """
    Check the bit-depth of a given image

    :param subject_image: The image that will have bit-depth checked
    :type subject_image: String
    :return: Boolean corresponding to 16 and 8 bit
    """
    # load an image
    subject = Image.open(subject_image)

    # if 16bit return false
    if subject.mode == 'I' or 'I;16':
        return False
    # if 8bit return true
    elif subject.mode == 'L':
        return True


def collect_greyscale_pixels(target_image):
    """
    Function to collect the individual pixel values for a given image

    :param target_image: The image that will have its pixel values collected
    :type target_image: String
    :return: Numpy array with size equal to resolution of target_image containing individual pixel values
    """
    image = Image.open(target_image)

    # if 8bit image run standard collection procedure
    if find_mode(target_image) is 'L':
        return np.array(image.getdata()).reshape(image.size)
    # if 16bit must first convert and then proceed with collection procedure
    elif find_mode(target_image) is 'I':
        return np.array(image.convert('I;16').getdata()).reshape(image.size)
    # error zero return
    else:
        return np.array(image.getdata()).reshape(image.size)


def convert_16bit_to_8bit(image_array):
    """
    Function to convert a 16-bit image to an 8-bit image

    :param image_array: An array of individual pixel values
    :type image_array: Array
    :return: An array oif individual pixel values between 0 and 255
    """
    # function to handle converting 16bit pixel range (0 - 65536)
    # to 8bit range (0-255)
    return (image_array * 1) / 256


def write_pixel_values(image_array, save_file):
    """
    Function to write an array of pixel values to a file

    :param image_array: The array containing individual pixel values of an image
    :param save_file: The name of the file to be written to
    """
    # debugging purposes
    with open(save_file, 'w') as file:
        file.write(str(image_array))


def calculate_mse(perfect_reference_image, subject_image):
    """
    Function to calculate the mean sqaured error of two images

    :param perfect_reference_image: The original 'perfect' reference image
    :param subject_image: The compressed image to have mse calculated for
    :return: The mean squared error of the compressed image
    """
    return mean_squared_error(check_colour_depth(perfect_reference_image),
                              check_colour_depth(subject_image))


def calculate_psnr(perfect_reference_image, subject_image):
    """
    Function to calulate the peak signal to noise ratio between two images

    :param perfect_reference_image: The original 'perfect' reference image
    :param subject_image: The compressed image to have psnr calculated for
    :return: The peak signal to noise ratio of the compressed image
    """
    # peak signal val = 255 for 8bit, and 65536 for 16bit
    return (10 * (np.log10(65536 ** 2))) / calculate_mse(perfect_reference_image, subject_image)


def calculate_ssim(perfect_reference_image, subject_image):
    """
    Function to calculate the Structural Similarity Index between two images

    :param perfect_reference_image: The original 'perfect' reference image
    :param subject_image: The copressed image to have SSIM calculated for
    :return: The SSIM of the compressed image
    """
    return ssim(perfect_reference_image, subject_image)


def calculate_difference(original_image, new_image):
    """
    Function to calculate the absolute difference between two arrays of pixel values

    :param original_image: An array of pixel values from the original image
    :param new_image: An array of pixel values from the compressed image
    :return: A third array containing the absolute difference between original_image and new_image
    """
    # load an original image
    original_pixel_vals = np.array(collect_greyscale_pixels(original_image))
    # and a compressed version
    new_pixel_vals = np.array(collect_greyscale_pixels(new_image))

    # check the images arent 16bit
    if not check_colour_depth(original_image):
        original_pixel_vals = convert_16bit_to_8bit(original_pixel_vals)

    # if they are convert to 8bit value range
    if not check_colour_depth(new_image):
        new_pixel_vals = convert_16bit_to_8bit(new_pixel_vals)

    # subtract the pixel values with goal of creating Absolute Difference Map
    return abs(np.array(original_pixel_vals - new_pixel_vals))


def load_raw_image(raw_image_file):
    """
    Function to generate array of individual pixel values from raw data file of an image
    usually in .dat format

    :param raw_image_file: The raw image file to be loaded
    :return: Numpy array of individual pixel values
    """
    image = np.fromfile(raw_image_file, dtype=np.uint16)
    # filler = np.zeros(shape=(1, 33), dtype=np.uint16)
    # image = np.append(arr=image, values=filler)
    image.shape = (int(np.sqrt(len(image))), int(np.sqrt(len(image))))
    return image


def calculate_averages():
    """
    Function to calculate and display the averages for difference in file sizes of original
    and compressed image variants
    """
    # load data from csv for bpe and j2k
    bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 8, 13, 18], names=["original-size",
                                                                                   "compressed-size-8",
                                                                                   "decompressed-size-8",
                                                                                   "compressed-size-80",
                                                                                   "decompressed-size-80"],
                             skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
    j2k_values = pd.read_csv("j2k_data_csv.csv", usecols=[2, 3, 8], names=["original-size",
                                                                           "compressed-size-8",
                                                                           "compressed-size-80"],
                             skiprows=2, skip_blank_lines=True, dtype=np.float64).dropna()

    # calculate the differences in file sizes at each compression level for bpe and j2k
    size_difference_bpe_8x_compressed = np.array(bpe_values['original-size']) - \
                                        np.array(bpe_values['compressed-size-8'])
    size_difference_bpe_80x_compressed = np.array(bpe_values['original-size']) - \
                                         np.array(bpe_values['compressed-size-80'])
    size_difference_bpe_8x_decompressed = np.array(bpe_values['original-size']) - \
                                          np.array(bpe_values['decompressed-size-8'])
    size_difference_bpe_80x_decompressed = np.array(bpe_values['original-size']) - \
                                           np.array(bpe_values['decompressed-size-80'])

    size_difference_j2k_8x = np.array(j2k_values['original-size'] - j2k_values['compressed-size-8'])
    size_difference_j2k_80x = np.array(j2k_values['original-size'] - j2k_values['compressed-size-80'])

    # print the results
    print(f"=====BPE=====\n"
          f"Average file size difference at:\n"
          f"8x compression: {int(np.average(size_difference_bpe_8x_compressed))}\n"
          f"8x decompression: {int(np.average(size_difference_bpe_8x_decompressed))}\n"
          f"80x compression: {int(np.average(size_difference_bpe_80x_compressed))}\n"
          f"80x decompression: {int(np.average(size_difference_bpe_80x_decompressed))}\n"
          f"=====J2K=====\n"
          f"Average file size difference at:\n"
          f"8x compression: {int(np.average(size_difference_j2k_8x))}\n"
          f"80x compression: {int(np.average(size_difference_j2k_80x))}\n"
          f"=====STANDARD DEVIATIONS=====\n"
          f"Standard deviation of change in file size with:\n"
          f"BPE at 8x compression: {int(np.std(size_difference_bpe_8x_compressed))}\n"
          f"BPE at 80x compression: {int(np.std(size_difference_bpe_80x_compressed))}\n"
          f"BPE at 8x decompression: {int(np.std(size_difference_bpe_8x_decompressed))}\n"
          f"BPE at 80x decompression: {int(np.std(size_difference_bpe_80x_decompressed))}\n"
          f"\n"
          f"J2K at 8x compression: {int(np.std(size_difference_j2k_8x))}\n"
          f"J2K at 80x compression: {int(np.std(size_difference_j2k_80x))}")


def generate_box(algorithm):
    """
    Function to generate and display boxplots from MatPlotLib of desired data

    :param algorithm: The condition for the if staement (either BPE or J2K depending on which boxplot is required)
    """
    if algorithm.upper().strip() == "BPE":
        # load data
        bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
            "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8",
            "compress-ssim-8", "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80",
            "compress-ssim-80"], skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
        # process data
        size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
        size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
        plt.boxplot(size_difference_bpe_80x_compressed, labels=["File size difference from CCSDS 122.0-B-2 80x compression (MB)"])
        # draw box
        plt.show()
    elif algorithm.upper().strip() == "J2K":
        bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
            "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8",
            "compress-ssim-8", "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80",
            "compress-ssim-80"], skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
        j2k_values = pd.read_csv("j2k_data_csv.csv", usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], names=[
            "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8",
            "compress-ssim-8", "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80",
            "compress-ssim-80"], skiprows=2, skip_blank_lines=True, dtype=np.float64).dropna()
        size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
        size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
        size_difference_j2k_8x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-8"])
        size_difference_j2k_80x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-80"])
        plt.boxplot([size_difference_bpe_80x_compressed, size_difference_j2k_80x_compressed], labels=["BPE x80 change in file size (MB)", "J2K x80 change in file size (MB)"])
        plt.show()
    else:
        print("Use algorithm abbreviations (bpe/j2k)")


def generate_scatter():
    """
    Function to generate scatter graphs for data representation
    """
    # load data
    bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
    j2k_values = pd.read_csv("j2k_data_csv.csv", usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=2, skip_blank_lines=True, dtype=np.float64).dropna()

    # all scatters of difference in file size (original and compressed) against...
    size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
    size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
    size_difference_j2k_8x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-8"])
    size_difference_j2k_80x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-80"])

    # plot scatter
    plt.scatter(j2k_values["compress-mse-8"], j2k_values["compress-psnr-8"], c="blue")
    plt.xlabel("MSE")
    plt.ylabel("PSNR")
    plt.show()
    # CCSDS 122.0-B-2


def print_stats():
    """
    Function to print the computed stats found in the report
    """
    # load data
    bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
    j2k_values = pd.read_csv("j2k_data_csv.csv", usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=2, skip_blank_lines=True, dtype=np.float64).dropna()

    # calculate size differences
    size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
    size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
    size_difference_j2k_8x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-8"])
    size_difference_j2k_80x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-80"])

    # pearsons correlation coefficient
    print(stats.pearsonr(size_difference_bpe_8x_compressed, bpe_values["compress-time-8"]))
    print(stats.pearsonr(size_difference_bpe_80x_compressed, bpe_values["compress-time-80"]))
    print(stats.pearsonr(size_difference_j2k_8x_compressed, j2k_values["compress-time-8"]))
    print(stats.pearsonr(size_difference_j2k_80x_compressed, j2k_values["compress-time-80"]))

    # print(max(bpe_values["compress-time-8"]))
    # print(max(bpe_values["compress-time-8"]) - min(bpe_values["compress-time-80"]))

    # print(max(j2k_values["compress-time-8"]))
    # print(max(j2k_values["compress-time-8"]) - min(j2k_values["compress-time-8"]))

    # two sample t-test
    print(stats.ttest_ind(bpe_values["compress-size-80"], j2k_values["compress-size-80"]))


def main():
    difference_vals = calculate_difference("AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_L01_00.png",
                                          "AUPE_images_for_compression_tests/ACE_outside_2xpct/j2k_compress/P00_T00_L01_00_80.j2k")
    print(np.max(difference_vals))
    image = Image.fromarray(difference_vals)
    image.show()

    # calculate_averages()
    # generate_box("j2k")
    # generate_scatter()


if __name__ == '__main__':
    main()
