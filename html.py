import header as hd
import footer as ft
import main
import datetime
from general_func import *

path = input("Path to image ->")

time_1 = datetime.datetime.now()
file_header, file_main, file_footer = marking_up(path)

text_header = hd.header_gen(file_header)
text_main = main.main_gen(file_main)
text_footer = ft.footer_gen(file_footer)

start_lines = ['<!DOCTYPE html>\n', '<html lang="en" dir="ltr">\n', '<head>\n', '  <title>Basic 90</title>\n', \
			   '  <meta charset="iso-8859-1">\n',
			   '  <link rel="stylesheet" href="styles/layout.css" type="text/css">\n', \
			   '</head>\n', '<body>\n']

with open('compiled_html_files/test_example.html', mode='w') as test:
	test.writelines(start_lines)

with open('compiled_html_files/test_example.html', mode='a') as test:
	test.writelines(text_header)
	test.writelines(text_main)
	test.writelines(text_footer)

time_2 = datetime.datetime.now()
print(f'Working time -> {time_2 - time_1}')
