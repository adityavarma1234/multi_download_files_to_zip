import requests

class UrlFilter:
	def __init__(self, urls):
		self.urls = urls
		self.filtered_urls = []

	def filter(self):
		for url in self.urls:
			if(self.is_downloadable(url)):
				self.filtered_urls.append(url)
		return self.filtered_urls

	def is_downloadable(self, url):
		response = requests.head(url)
		header = response.headers
		content_type = header.get('content-type')
		if content_type.lower() in ['text', 'html']:
			return False
		return True