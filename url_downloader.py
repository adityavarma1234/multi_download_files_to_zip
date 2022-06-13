import sys, os
import zipfile
import requests
import uuid
from multiprocessing import Pool, cpu_count
from multiprocessing.pool import ThreadPool
from functools import partial
from io import BytesIO

from zip_helper import ZipHelper
from status_values import StatusValues

class UrlDownloader:
	def __init__(self, urls):
		self.urls = urls
		self.uuid = str(uuid.uuid4())
		self.create_dir()

	def create_dir(self):
		self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download_data', self.uuid)
		self.zip_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zip_data')	
		try:
			if not os.path.exists(self.file_path):
				os.makedirs(self.file_path)
			if not os.path.exists(self.zip_file_path):
				os.makedirs(self.zip_file_path)
		except Exception as e:
			print("Exception in creating dir ", e)

	def uuid(self):
		return self.uuid

	def fetch_pool(self):
		return ThreadPool(cpu_count() - 1)

	def download_url(self, url):
		print("file_path: ", self.file_path)
		print("downloading: ", url)
		# TODO: Add retry logic for network errors
		try:
			file_name = os.path.join(self.file_path, url.split("/")[-1])
			response = requests.get(url, stream=True)
			if response.status_code == requests.codes.ok:
				with open(file_name, 'wb') as f:
					f.write(response.content)
			else:
				# TODO for different status code check errors
				val = 1
		except Exception as e:
			print(e)
		return url

	def download(self):
		pool = self.fetch_pool()
		# TODO: check if url is downloadable or not: https://gist.github.com/Bharat-B/796ea2c1b17fe3d63ad39258a84b384d
		results = pool.imap_unordered(self.download_url, self.urls)
		for r in results:
			print(r)

	def zip_files(self):
		zip_file_path = os.path.join(self.zip_dir_path, self.uuid)
		ZipHelper(self.file_path, zip_file_path).zip()
		print('zip of files completed')

urls = [
'https://www.northwestknowledge.net/metdata/data/pr_1979.nc',
 'https://www.northwestknowledge.net/metdata/data/pr_1980.nc'
]
# url_downloader = UrlDownloader(urls)
# url_downloader.download()
# url_downloader.zip_files()