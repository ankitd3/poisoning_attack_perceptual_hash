# The MIT License (MIT)
#
# Copyright (c) 2017 Mihir Wagle
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PIL import Image
from pycipher import Vigenere
import getopt, sys, math, os, struct, timeit

# Number of least significant bits containing/to contain data in image
num_lsb = 2

def prepare_hide():
    # Prepare files for reading and writing for hiding data.
    global image, input_file

    try:
        image = Image.open(input_image_path)
        input_file = open(input_file_path, "rb")
        #print (input_file.read())
    except FileNotFoundError:
        print("Input image or file not found, will not be able to hide data.")

def prepare_recover():
    # Prepare files for reading and writing for recovering data.
    global steg_image, output_file

    try:
        steg_image = Image.open(steg_image_path)
        output_file = open(output_file_path, "wb+")
    except FileNotFoundError:
        print("Steg image not found, will not be able to recover data.")

def reset_buffer():
    global buffer, buffer_length

    buffer = 0
    buffer_length = 0

def and_mask(index, n):
    # Returns an int used to set n bits to 0 from the index:th bit when using
    # bitwise AND on an integer of 8 bits or less.
    # Ex: and_mask(3,2) --> 0b11100111 = 231.
    return 255 - ((1 << n) - 1 << index)

def get_filesize(path):
    # Returns the filesize in bytes of the file at path
    return os.stat(path).st_size

def max_bits_to_hide(image):
    # Returns the number of bits we're able to hide in the image
    # using num_lsb least significant bits.
    # 3 color channels per pixel, num_lsb bits per color channel.
    return int(3 * image.size[0] * image.size[1] * num_lsb)

def bits_in_max_filesize(image):
    # Returns the number of bits needed to store the size of the file.
    return max_bits_to_hide(image).bit_length()

def read_bits_from_buffer(n):
    # Removes the first n bits from the buffer and returns them.
    global buffer, buffer_length

    bits = buffer % (1 << n)
    buffer >>= n
    buffer_length -= n
    return bits

def recover_data():
    # Writes the data from the steganographed image to the output file
    global buffer, buffer_length, steg_image

    start = timeit.default_timer()
    prepare_recover()
    reset_buffer()

    data = bytearray()

    color_data = list(steg_image.getdata())
    color_data_index = 0

    pixels_used_for_filesize = math.ceil(bits_in_max_filesize(steg_image)
                                         / (3 * num_lsb))
    for i in range(pixels_used_for_filesize):
        rgb = list(color_data[color_data_index])
        color_data_index += 1
        for i in range(3):
            # Add the num_lsb least significant bits
            # of each color channel to the buffer.
            buffer += (rgb[i] % (1 << num_lsb) << buffer_length)
            buffer_length += num_lsb

    # Get the size of the file we need to recover.
    bytes_to_recover = read_bits_from_buffer(bits_in_max_filesize(steg_image))
    print("Looking to recover", bytes_to_recover, "bytes")

    while (bytes_to_recover > 0):
        rgb = list(color_data[color_data_index])
        color_data_index += 1
        for i in range(3):
            # Add the num_lsb least significant bits
            # of each color channel to the buffer.
            buffer += (rgb[i] % (1 << num_lsb)) << buffer_length
            buffer_length += num_lsb

        while (buffer_length >= 8 and bytes_to_recover > 0):
            # If we have more than a byte in the buffer, add it to data
            # and decrement the number of bytes left to recover.
            bits = read_bits_from_buffer(8)
            data += struct.pack('1B', bits)
            bytes_to_recover -= 1
    data = bytes(data).decode('utf-8')
    decrypted = Vigenere(key).decipher(data)
    decrypted = decrypted.encode('utf-8')
    output_file.write(decrypted)
    output_file.close()

    stop = timeit.default_timer()
    print("Runtime: {0:.2f} s".format(stop - start))

def analysis():
    # Find how much data we can hide and the size of the data to be hidden
    prepare_hide()
    print("Image resolution: (", image.size[0], ",", image.size[1], ")")
    print("Using", num_lsb, "LSBs: we can hide\t",
          max_bits_to_hide(image) // 8, "B")
    print("Size of input file: \t\t", get_filesize(input_file_path), "B")
    print("Filesize tag: \t\t\t",
          math.ceil(bits_in_max_filesize(image) / 8), "B")


hiding_data = False
recovering_data = True

key = 'MSW'
compression = 1

# Initial paths, variables used.
#input_image_path = "pic.png"
#steg_image_path = "steg_image.png"
#input_file_path = "a.txt"
#output_file_path = "b.txt"
#key = "MihirWagle"
#compression = 1
