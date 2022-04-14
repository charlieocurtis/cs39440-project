from PIL import Image
from sklearn.metrics import mean_squared_error
from skimage.metrics import structural_similarity as ssim

import sys
import numpy as np

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
        return convert_16bit_to_8bit(collect_greyscale_pixels(subject_image))
    # if 8bit return true
    elif subject.mode == 'L':
        return collect_greyscale_pixels(subject_image)


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
    return (10 * (np.log10(255 ** 2))) / calculate_mse(perfect_reference_image, subject_image)


def calculate_ssim(perfect_reference_image, subject_image):
    # function to calculate Structural Similarity Index
    return ssim(perfect_reference_image, subject_image)


def calculate_difference(original_image, new_image):
    # load an original image
    original_pixel_vals = collect_greyscale_pixels(original_image)
    # and a compressed version
    new_pixel_vals = collect_greyscale_pixels(new_image)

    # check the images arent 16bit
    if not check_colour_depth(original_image):
        original_pixel_vals = convert_16bit_to_8bit(original_pixel_vals)

    # if they are convert to 8bit value range
    if not check_colour_depth(new_image):
        new_pixel_vals = convert_16bit_to_8bit(new_pixel_vals)

    # subtract the pixel values with goal of creating Absolute Difference Map
    return new_pixel_vals - original_pixel_vals


def load_raw_image(raw_image_file):
    image = np.fromfile(raw_image_file, dtype=np.uint16)
    # filler = np.zeros(shape=(1, 33), dtype=np.uint16)
    # image = np.append(arr=image, values=filler)
    image.shape = (int(np.sqrt(len(image))), int(np.sqrt(len(image))))
    return image


def main():
    # print(find_mode("sample_images/LWAC01_compression_10.j2k"))
    # print(check_colour_depth("sample_images/LWAC01_compression_10.j2k"))
    # print(np.array(Image.open("sample_images/LWAC01_compression_10.j2k").getdata()))
    # generated_image = np.asarray(calculate_difference("test_image.png",
    #                                                   "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"))
    # created_image = Image.fromarray(generated_image)
    # print(calculate_psnr(generated_image))
    # created_image.show()

    # image = "sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"
    # find_mode(image)

    # image = Image.fromarray(load_raw_image("sample_images/LWAC01_uncompressed_image_raw.dat"))
    # image.save("LWAC01_uncompressed_image.png")
    # print(load_raw_image("LWAC01_outfile_compressed.dat"))
    # print(image.size)
    # image.show()

    # image = Image.fromarray(load_raw_image(
    #     "for_quality_calcs/acli_sandpit_rocks/comptest_objects2-sandpit2_LWAC01_T00_P00_compressed_1.uncompressed.dat"))
    # # image.show()
    # image.save("for_quality_calcs/acli_sandpit_rocks/comptest_objects2-sandpit2_LWAC01_T00_P00_compressed_1.uncompressed.png")

    # print(load_raw_image("sample_images/LWAC01_outfile_compressed.dat"))

    print("MSE: ")
    print(calculate_mse(
        "AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_R01_00.png",
        "for_quality_calcs/ACE_outside_2xpct/P00_T00_R01_00_compressed_0.1.uncompressed.png"))
    print("PSNR: ")
    print(f"{calculate_psnr('AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_R01_00.png', 'for_quality_calcs/ACE_outside_2xpct/P00_T00_R01_00_compressed_0.1.uncompressed.png')} dB")
    print("SSIM:")
    print(calculate_ssim(check_colour_depth('AUPE_images_for_compression_tests/ACE_outside_2xpct/pre-compression/P00_T00_R01_00.png'), check_colour_depth("for_quality_calcs/ACE_outside_2xpct/P00_T00_R01_00_compressed_0.1.uncompressed.png")))

    # print(collect_greyscale_pixels("LWAC01_JPG_to_PNG.png"))
    # print(convert_16bit_to_8bit(collect_greyscale_pixels_16bit("sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png")))
    # png_to_bmp("LWAC01_JPG_to_PNG.png", "LWAC01_JPG_to_BMP.bmp")
    # print(find_mode("sample_images/comptest_objects2-sandpit2_LWAC01_T00_P00.png"))

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
