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
    # find the current mode of the required image
    image = Image.open(subject_image)
    return image.mode


def check_colour_depth(subject_image):
    # load an image
    subject = Image.open(subject_image)

    # if 16bit return false
    if subject.mode == 'I' or 'I;16':
        return False
    # if 8bit return true
    elif subject.mode == 'L':
        return True


def collect_greyscale_pixels(target_image):
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
    # function to handle converting 16bit pixel range (0 - 65536)
    # to 8bit range (0-255)
    return (image_array * 1) / 256


def write_pixel_values(image_array, save_file):
    # debugging purposes
    # writing collected image pixel vals to text file
    with open(save_file, 'w') as file:
        file.write(str(image_array))


def calculate_mse(perfect_reference_image, subject_image):
    # function to calculate Mean Squared Error
    return mean_squared_error(check_colour_depth(perfect_reference_image),
                              check_colour_depth(subject_image))


def calculate_psnr(perfect_reference_image, subject_image):
    # function to calculate Peak Signal to Noise Ratio
    # peak signal val = 255 for 8bit, and 65536 for 16bit
    return (10 * (np.log10(65536 ** 2))) / calculate_mse(perfect_reference_image, subject_image)


def calculate_ssim(perfect_reference_image, subject_image):
    # function to calculate Structural Similarity Index
    return ssim(perfect_reference_image, subject_image)


def calculate_difference(original_image, new_image):
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
    image = np.fromfile(raw_image_file, dtype=np.uint16)
    # filler = np.zeros(shape=(1, 33), dtype=np.uint16)
    # image = np.append(arr=image, values=filler)
    image.shape = (int(np.sqrt(len(image))), int(np.sqrt(len(image))))
    return image


def calculate_averages():
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
    # For boxplots of real time at both compression ratios for BPE and j2k
    if algorithm.upper().strip() == "BPE":
        bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
            "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8",
            "compress-ssim-8", "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80",
            "compress-ssim-80"], skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
        size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
        size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
        plt.boxplot(size_difference_bpe_80x_compressed, labels=["File size difference from CCSDS 122.0-B-2 80x compression (MB)"])
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
    bpe_values = pd.read_csv("bpe_data_csv.csv", usecols=[2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=3, skip_blank_lines=True, dtype=np.float64).dropna()
    j2k_values = pd.read_csv("j2k_data_csv.csv", usecols=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], names=[
        "original-size", "compress-size-8", "compress-time-8", "compress-mse-8", "compress-psnr-8", "compress-ssim-8",
        "compress-size-80", "compress-time-80", "compress-mse-80", "compress-psnr-80", "compress-ssim-80"],
                             skiprows=2, skip_blank_lines=True, dtype=np.float64).dropna()

    size_difference_bpe_8x_compressed = np.array(bpe_values["original-size"] - bpe_values["compress-size-8"])
    size_difference_bpe_80x_compressed = np.array(bpe_values['original-size'] - bpe_values['compress-size-80'])
    size_difference_j2k_8x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-8"])
    size_difference_j2k_80x_compressed = np.array(j2k_values["original-size"] - j2k_values["compress-size-80"])

    plt.scatter(j2k_values["compress-mse-8"], j2k_values["compress-psnr-8"], c="blue")
    plt.xlabel("MSE")
    plt.ylabel("PSNR")
    plt.show()
    # CCSDS 122.0-B-2

    # print(stats.pearsonr(size_difference_bpe_8x_compressed, bpe_values["compress-time-8"]))
    # print(stats.pearsonr(size_difference_bpe_80x_compressed, bpe_values["compress-time-80"]))
    # print(stats.pearsonr(size_difference_j2k_8x_compressed, j2k_values["compress-time-8"]))
    # print(stats.pearsonr(size_difference_j2k_80x_compressed, j2k_values["compress-time-80"]))

    # print(max(bpe_values["compress-time-8"]))
    # print(max(bpe_values["compress-time-8"]) - min(bpe_values["compress-time-80"]))
    #
    # print(max(j2k_values["compress-time-8"]))
    # print(max(j2k_values["compress-time-8"]) - min(j2k_values["compress-time-8"]))

    # print(stats.ttest_ind(bpe_values["compress-size-80"], j2k_values["compress-size-80"]))


def main():
    # print(find_mode("AUPE_images_for_compression_tests/acli_sandpit_rocks/pre-compression/comptest_objects2-sandpit2_LWAC01_T00_P00.png"))
    # print(check_colour_depth("sample_images/LWAC01_compression_10.j2k"))
    # print(np.array(Image.open("sample_images/LWAC01_compression_10.j2k").getdata()))
    # generated_image = np.asarray(calculate_difference("test_image.png",
    #                                                   "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"))
    # created_image = Image.fromarray(generated_image)
    # print(calculate_psnr(generated_image))
    # created_image.show()
    # image = "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"
    # find_mode(image)

    difference_vals = calculate_difference("AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_L01_00.png",
                                          "AUPE_images_for_compression_tests/ACE_outside_2xpct/j2k_compress/P00_T00_L01_00_80.j2k")
    print(np.max(difference_vals))
    image = Image.fromarray(difference_vals)
    image.show()

    # calculate_averages()
    # generate_box("j2k")
    # generate_scatter()


    # image = Image.fromarray(load_raw_image(
    #     "collated/acli_sandpit_rocks/compress_0.1/comptest_objects2-sandpit2_RWAC01_T00_P00_compressed_0.1.decoded.dat"))
    # image.show()
    # image.save("collated/acli_sandpit_rocks/compress_0.1/comptest_objects2-sandpit2_RWAC01_T00_P00_compressed_0.1.decoded.png")

    # print(load_raw_image("sample_images/LWAC01_outfile_compressed.dat"))

    # print("MSE: ")
    # print(calculate_mse("AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_L01_00.png",
    #                     "collated/ACE_outside_2xpct/compress_0.1/P00_T00_L01_00_compressed_0.1.decoded.png"))
    # print("PSNR: ")
    # print(calculate_psnr('AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_L01_00.png',
    #                      'collated/ACE_outside_2xpct/compress_0.1/P00_T00_L01_00_compressed_0.1.decoded.png'))
    # print("SSIM:")
    # print(calculate_ssim(
    #     check_colour_depth('AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_L01_00.png'),
    #     check_colour_depth("collated/ACE_outside_2xpct/compress_0.1/P00_T00_L01_00_compressed_0.1.decoded.png")))

    # print(collect_greyscale_pixels("LWAC01_JPG_to_PNG.png"))
    # print(convert_16bit_to_8bit(collect_greyscale_pixels_16bit("sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png")))
    # png_to_bmp("LWAC01_JPG_to_PNG.png", "LWAC01_JPG_to_BMP.bmp")
    # print(find_mode("L0123-Composite.png"))

    # write_pixel_values(collect_greyscale_pixels("LWAC01_JPG_to_BMP.bmp"), "test-output.txt")

    # print(calculate_difference("LWAC01_JPG.jpg", "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"))

    # sample_array = calculate_difference("sample_images/test_j2k_compress_out.j2k", "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png")
    # sample_image = Image.fromarray(sample_array, mode='L')
    # sample_image.show()
    # print(sample_array)

    # print(collect_greyscale_pixels("saved-image.png"))
    # convert_image_format("LWAC02_JPG.jpg", "LWAC02_JPG_to_PNG.png")

    # print(calculate_mse("LWAC01_JPG_to_PNG.png", "LWAC01_JPG_to_BMP.bmp"))

    # test_vals = collect_luminance_vals_8bit("test_image.png")
    # write_luminance_vals(LUMINANCE_WRITE, test_vals)
    # png_to_jpg_8bit("test_image.png", "test_image.jpg")
    # write_luminance_vals("jpg-luminance-out.txt", collect_luminance_vals_8bit("test_image.jpg"))

    # convert_grey_8bit_png("test_image.png")


if __name__ == '__main__':
    main()
