"""
A web crawler to gather data from specific Zimbabwean websites that offer content in native languages
"""

import requests
import bs4
from time import sleep as wait

'''
The Problem I have faced is that the content per page is limited, and there is a "Load more" link. So I am going to automate the clicking of that link button
a jillion times :D
'''


# headers for the spider
headers = {'ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', 'ACCEPT_ENCODING':'gzip, deflate, br', 
	'ACCEPT_LANGUAGE': 'en-US,en;q=0.9', 'CONNECTION': 'keep alive', 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

# urls for the websites
voa_url = 'https://www.voandebele.com'
kwayedza_url = 'http://kwayedza.co.zw'



# first step is to get the links from the main page using the requests module
print('****************************************************************')
print('    Web crawler for gathering data from kwayedza and VOANdebele. Purpose is for gathering text to feed as a dataset to my Neural nets :D ')
print(' STARTING VOANdebele.com ')
print('*****************************************************************')
# since we want data from the button comes in pages, we want to automatically change the pages.
for page_index in range(1, 5):
	second_request = requests.get(voa_url + '/z/3178?p=' + str(page_index), headers=headers)
	print('[*] Parsing link : ', voa_url + '/z/3178?p=' + str(page_index))

	# parse the text acquired from the requests object
	voa_text = second_request.text

	# Passing the acquired text as html to beautiful soup
	html_voa = bs4.BeautifulSoup(voa_text, 'lxml')


	# starting with the VOA item, we are going to extract the links to the articles that contain the Ndebele language text.
	# first we have to get the <div class="small-thums-list follow-up-list"></div> since its the parent of the List of links

	voa_parent_div = html_voa.find(class_="small-thums-list follow-up-list")


	for link in voa_parent_div.find_all('a', class_='img-wrap'):
		article_page_link = voa_url + link.get('href')
		article_page = requests.get(article_page_link, headers=headers)
		print('[+] Found link: ', link.get('href'))

		# Now that we have the link to each article, we can visit the article and crawl it using beautiful soup
		article_page_content = bs4.BeautifulSoup(article_page.text, 'lxml')

		with open('voa_data.txt', 'a+') as voa_file:
			# this div contains the paragraphs that make up the content article <div class="wsw"></div>
			voa_article_div = article_page_content.find('div', class_='wsw')
			
			print('[+] Writing data for link to file..')

			# getting all the paragraphs in the article div
			for paragraph in voa_article_div.find_all('p'):
				# open a text file and write the text in the paragraphs
				voa_file.write(paragraph.get_text())

			# close the opened file

			voa_file.close()


print('[***] Done with VOANdebele.')
print('***************************** KWAYEDZA ************************************************')

# Restarting the process all over again, the difference being that this time I am extracting data from Kwayedza website instead :D
for second_index in range(1, 5):

	# take the text from the first 4 pages of Kwayedza
	first_request = requests.get(kwayedza_url + '/category/nhau-dzemuno/page/' + str(second_index) + '/', headers=headers)
	print('[*] Parsing Link: ', kwayedza_url + '/category/nhau-dzemuno/page/' + str(second_index) + '/')

	# pass the text from the webpage so we can find links 
	kwayedza_text = first_request.text
	html_kwayedza = bs4.BeautifulSoup(kwayedza_text, 'lxml')

	# Get the <div class="row listing"></div> so we can search the paginated links
	row_listing_div = html_kwayedza.find('div', class_='row listing')

	"""
	The structure of the html looks like the following: 

	 <div class="row listing">
		<div class="column half">
			<article>
				<span></span>
				<a></a>
			</article>
		</div>
	 </div>

	 So basically we want to get the <a></a> tags since they contain  the links to the articles

	"""
	for column in row_listing_div.find_all('div', class_='column half'):
		# get the a tag
		link_tag = column.find('a', class_='image-link')
		print('[+] Found link: ', link_tag.get('href'))

		page_link_request = requests.get(link_tag.get('href'), headers=headers)

		# parse the request as html
		html_kwayedza_article = bs4.BeautifulSoup(page_link_request.text, 'lxml')


		article_parent_div = html_kwayedza_article.find('div', class_='post-content-right')

		for paragraph in article_parent_div.find_all('p'):

			# finally write the contents to a text file 
			with open('kwayedza_data.txt', 'a+') as kwayedza_file:
				print('[+] Writing paragraph to file....')
				kwayedza_file.write(paragraph.get_text())

			print('---------------------------------------------------------------')

	print('[+] Completed Parsing Link')


print('************************ DONE SCRAPPING ********************************************')


