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
from url_filter import UrlFilter

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
			if not os.path.exists(self.zip_dir_path):
				os.makedirs(self.zip_dir_path)
		except Exception as e:
			print("Exception in creating dir ", e)

	def uuid(self):
		return self.uuid

	def fetch_pool(self):
		return ThreadPool(cpu_count() - 1)

	def download_url(self, url, global_status_hash):
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
			self.global_status_hash[self.uuid] = "ErrorCode:102"
		return url



	def download(self, global_status_hash):
		len_urls = len(self.urls)
		filtered_urls = UrlFilter(urls).filter()
		filtered_urls_length = len(filtered_urls)

		if(len_urls != filtered_urls_length):
			global_status_hash[self.uuid] = "ErrorCode:100"
			return False


		pool = self.fetch_pool()
		## This can be avoided by using a db and updating the corresponding error code
		self.global_status_hash = global_status_hash
		results = pool.imap_unordered(self.download_url, self.urls)
		for r in results:
			print(r)
		return True

	def zip_files(self, global_status_hash):
		zip_file_path = os.path.join(self.zip_dir_path, self.uuid)
		try:
			ZipHelper(self.file_path, zip_file_path).zip()
			print('zip of files completed')
		except Exception as e:
			global_status_hash[self.uuid] = "ErrorCode:101"
			return False
		return True

urls = [
'https://www.northwestknowledge.net/metdata/data/pr_1979.nc',
 'https://www.northwestknowledge.net/metdata/data/pr_1980.nc'
]
# url_downloader = UrlDownloader(urls)
# url_downloader.download()
# url_downloader.zip_files()