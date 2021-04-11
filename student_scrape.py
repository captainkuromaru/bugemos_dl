#!/usr/bin/env python
# student_scrape
# downloads Student comic strips, super basic script
import re
import requests
from bs4 import BeautifulSoup
from os.path import basename

def main(pocitadlo, i):
	# if something is fudged
	if (pocitadlo == 0) & (i == 0):
		pocitadlo = 243
		i = 1
	# the webpage where we look for the images
	web_url = 'https://www.bugemos.com/?q=node/' + str(pocitadlo)
	html_text = requests.get(web_url).text
	soup = BeautifulSoup(html_text, 'html.parser')
	imgs = soup.find_all("img")
	# go through all images
	for img in imgs:
		# find Student comic strips
		if re.search('komiksy/Student/', img.get('src')):
			# format is last part of the url containing a period (".") and letters (e.g. jpg, gif)
			format = re.findall('\.[a-z]*$', img.get('src'))
			format = format[0]
			# call download function with url of the image, its format, and number
			download_img(img.get('src'), format, i)
			# increment the strip number
			i = i+1
	# increment pocitadlo when done
	pocitadlo = pocitadlo+1
	# that's the last page with Student comic strips
	if pocitadlo<=358:
		# if there are comic strips left, call the function again
		main(pocitadlo,i)
	else:
		# if not, exit
		print("Done")
		exit(0)

def download_img(img_url, format, i):
	# create the url for download
	url = "https://www.bugemos.com/" + img_url
	# number of the strip plus its type
	filename = str(i) + format

	req = requests.get(url)
	# open (write) file
	with open(filename, 'wb') as f:
		f.write(req.content)
	print('Downloaded: ' + url + ', ' + filename)

if __name__ == "__main__":
    main(243,1)
