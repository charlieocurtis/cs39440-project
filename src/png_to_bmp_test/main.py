from PIL import Image
import numpy as np

# collect the png file
png_input = "test_image.png"
image = Image.open(png_input)

# convert the png into bmp
bmp_output = "test_image.bmp"
image.save(bmp_output)

# collect the bmp
bmp_collection = Image.open(bmp_output)
# collect each pixel rgb values and put into list
# in the case of png image this also contains alpha field
bmp_pix_vals = list(bmp_collection.getdata())

# write each tuple to the output file ready to be read and compared with original
with open("output.txt", "w") as file:
    for rgb in bmp_pix_vals:
        file.write(str(rgb)[1:-1])
        file.write("\n")

# converts image to grey scale and then collects luminance values
# can now calculate MSE
luminance = np.asarray(bmp_collection.convert("L"))

counter = 0

# counter is for debugging purposes when trying to establish
# how the library is outputting data into the given text file
with open("luminance-out.txt", "w") as file:
    for line in luminance:
        file.write(str(line))
        file.write("\n")
        counter += 1

# when printing luminance values for bmp version of image
# the correct dimensions are printed to text file
print(counter)
# print(f"{luminance}\n")


