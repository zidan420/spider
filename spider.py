import re, argparse
from requests import *
from threading import Thread
from urllib.parse import urljoin # import urlparse (in python2)


# def request_url(url):
# 	try:
# 		return get("http://" + url)
# 	except exceptions.ConnectionError:
# 		pass

def extract_link_from(url):
	response = get(url)
	try:
		response = response.content.decode('utf-8')
		return re.findall('(?:href=")(.*?)"', response)
	except:
		return []

def crawl(url):
	href_links = extract_link_from(url)
	for link in href_links:
		link = urljoin(url, link)

		if "#" in link:
			link = link.split("#")[0]
		
		if url in link and link not in target_links:
			target_links.append(link)
			print(link)
			t = Thread(target=crawl, args=(link,))
			t.start()

def main():
	global target_links
	target_links = []
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--target', help="Specify the Target URL")
	args = parser.parse_args()
	target_url = args.target
	crawl(target_url)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		exit()