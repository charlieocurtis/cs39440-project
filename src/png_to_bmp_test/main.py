from PIL import Image

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


