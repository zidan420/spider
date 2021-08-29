import re, argparse, requests
from threading import Thread
from urllib.parse import urljoin

def extract_link_from(url):
	try:
		response = requests.get(url)
		response = response.content.decode('utf-8')
		return re.findall('(?:href=")(.*?)"', response)
	except requests.exceptions.ConnectionError:
		print("[-] Connection could NOT be established! Please check if the link is correct.")
		exit()
	except requests.exceptions.RequestException:
		print("[-] Invalid URL. Are you missing 'http://' or 'https://'?")
		exit()
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
