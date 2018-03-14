"""
This a web crawler for downloading wallpapers from wallpaperscraft.com
"""

from bs4 import BeautifulSoup
import requests
import argparse
import sys, os

headers = {'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'ACCEPT_ENCODING':'gzip, deflate, br', 
	'ACCEPT_LANGUAGE': 'en-US,en;q=0.9', 'CONNECTION': 'keep alive', 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

def createUrl(catalog, resolution):
	return 'https://wallpaperscraft.com/catalog/' + catalog + '/' + resolution

def createPagedUrl(catalog, resolution, page_number):
	if page_number == 1:
		return createUrl(catalog, resolution)

	else:
		return createUrl(catalog, resolution) + '/page' + str(page_number)


def createRequest(url):
	return requests.get(url, headers=headers)

def downloadImage(save_name, image_request, folder_name='wallpapers'):
	print('[+] Saving as downloads/'+folder_name+'/', save_name)
	with open('downloads/'+folder_name+'/' + save_name, 'wb') as img:
		img.write(image_request.content)


def getMaximumPaging(url):
	request_object = createRequest(url)
	nums_list = []

	soup_object = BeautifulSoup(request_object.text, 'lxml')
	paging_div = soup_object.find('div', class_='pages')

	if paging_div is not None:
		for link in paging_div.find_all('a', class_='page_select'):
			nums_list.append(int(link.get_text()))
			


	return max(nums_list)



def main():

	argument_parser = argparse.ArgumentParser()

	argument_parser.add_argument("-c", "--catalog", required=True, help="catalogue of the wallpapers to download from")
	argument_parser.add_argument("-r", "--resolution", required=True, help="resolution of the wallpapers")
	argument_parser.add_argument("-p", "--page", required=True, help="number of pages available for this catalog")
	arguments = argument_parser.parse_args()
	
	catalog = arguments.catalog
	resolution = arguments.resolution
	page_number = arguments.page

	first_url = createUrl(catalog, resolution)

	max_paging = getMaximumPaging(first_url)

	if int(page_number) > max_paging:
		print('[!] You have specified waayyy too many pages than are available...')
		sys.exit(0)

	else:
		for index in range(2, int(page_number)):
			url = createPagedUrl(catalog, resolution, index)

			print('<=== Downloading the wallpapers ===>')

			list_request = createRequest(url)

			list_html = BeautifulSoup(list_request.text, 'lxml')

			wallpaper_list_div = list_html.find('div', class_='wallpapers')

			for div in wallpaper_list_div.find_all('div', class_='wallpaper_pre'):
				image_link = div.find('a', target='_blanck')

				full_image_url = 'https:' + image_link.get('href')

				image_request = createRequest(full_image_url)

				wallpaper_html = BeautifulSoup(image_request.text, 'lxml')

				wallpaper_div = wallpaper_html.find('div', class_='wb_preview')

				wallpaper_link = wallpaper_div.find('img').get('src')

				# print(wallpaper_link)


				wallpaper_link = 'https:' + wallpaper_link

				wallpaper_name_array = wallpaper_link.split('image/')

				save_name = wallpaper_name_array[1]

				wallpaper_request_object = createRequest(wallpaper_link)
				print('[*] Found Wallpaper: ', save_name)

				folder_name = catalog

				if not os.path.isdir(os.path.join(os.getcwd(), 'downloads/' + folder_name)):
					os.mkdir('downloads/' + folder_name)

				downloadImage(save_name, wallpaper_request_object, folder_name=folder_name)





if __name__ == '__main__':
	main()

