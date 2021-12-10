from os import listdir
from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
import keras.models as km
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input
import numpy as np
import re
from PIL import Image
from collections import Counter
import math


def rgb_to_hex(rgb):
	return '#%02x%02x%02x' % rgb


def get_popular_color_from_part(path):
	img = Image.open(path)
	size = img.size  # (x, y) - size of image

	pixels = img.load()
	lst_pixels = []

	for x in range(size[0]):
		for y in range(size[1]):
			lst_pixels.append(pixels[x, y])  # Создаем список с элементами равными цвету пикселя в RGB
	dict_pixels = Counter(lst_pixels)
	final_dict = dict([max(dict_pixels.items(), key=lambda k_v: k_v[1])])  # Наиболее часто используемый цвет
	color_rgb = list(final_dict.keys())[0]
	color_hex = rgb_to_hex(color_rgb)
	return color_hex


def get_popular_color_in_row(img, num_row):
	size = img.size  # (x, y) - size of image

	pixels = img.load()
	lst_pixels = []

	for y in [num_row]:
		for x in range(size[1]):
			lst_pixels.append(pixels[x, y])  # Создаем список с элементами равными цвету пикселя в RGB
	dict_pixels = Counter(lst_pixels)
	final_dict = dict([max(dict_pixels.items(), key=lambda k_v: k_v[1])])  # Наиболее часто используемый цвет
	color_rgb = list(final_dict.keys())[0]
	# color_hex = rgb_to_hex(color_rgb)
	return color_rgb


# marking up photos

def img_concat(path):
	img = Image.open(path)
	img_new = Image.new('RGB', (img.size[0], img.size[1] * 2))
	img_new.paste(img, (0, 0))
	img_new.paste(img, (0, img.size[1]))
	return img_new


def distance(first_color, second_color):
	distance = math.sqrt((first_color[0] - second_color[0]) ** 2 + \
						 (first_color[1] - second_color[1]) ** 2 + \
						 (first_color[2] - second_color[2]) ** 2)
	return distance


def marking_up(path):
	# Берем цвет первой строки, потом сравниваем следующие строки
	# Если нет ни одного совпадения, обрезаем фотку по этот пиксель
	# Берем цвет последней стоки, сравниваем снизу вверх и берем
	# так же как и до этого.
	# В итоге у нас осталась центральная часть, в ней мы идем вниз по
	# нужным пикселям и обрезаем фотку и в итоге разделяем
	# в центральной части итераций столько, сколько пикселей

	img = Image.open(path)
	size = img.size
	first_row_color = get_popular_color_in_row(img, 0)

	# Header
	pixels_first = img.load()
	index = 0
	for row in range(size[1]):
		count = 0
		for column in range(size[0]):
			pixel_color = pixels_first[column, row]
			if first_row_color == pixel_color:
				count += 1
			if distance(first_row_color, pixel_color) < 35:
				count += 1
		index += 1
		if count == 0:
			break

	img_header = img.crop((0, 0, size[0], index))
	img_after_header = img.crop((0, index, size[0], size[1]))

	# footer
	size = img_after_header.size
	pixels_second = img_after_header.load()
	last_row_color = get_popular_color_in_row(img_after_header, -1)
	index = 0

	for row in range(size[1] - 1, -1, -1):  # от y-1 (так как отсчет 0) до -1 (чтобы дойти до 0) с шагом -1
		count = 0
		for column in range(size[0] - 1, -1, -1):
			pixel_color = pixels_second[column, row]
			if last_row_color == pixel_color:
				count += 1
			if distance(last_row_color, pixel_color) < 35:
				count += 1
		index += 1
		if count == 0:
			break
	img_footer = img_after_header.crop((0, size[1] - index, size[0], size[1]))
	img_after_header_footer = img_after_header.crop((0, 0, size[0], size[1] - index - 1))

	img.save('cache/input_image.jpg')
	img_header.save('cache/output_header.jpg')
	header_path = 'cache/output_header.jpg'
	img_footer.save('cache/output_footer.jpg')
	footer_path = 'cache/output_footer.jpg'
	img_after_header_footer.save('cache/output_main.jpg')
	main_path = 'cache/output_main.jpg'

	return header_path, main_path, footer_path
