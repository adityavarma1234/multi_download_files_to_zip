import shutil

class ZipHelper:
	def __init__(self, dir_path_to_zip, output_filename):
		self.dir_path = dir_path_to_zip
		self.output_filename = output_filename

	def zip(self):
		shutil.make_archive(self.output_filename, 'zip', self.dir_path)

# ZipHelper('/Users/aditya/Documents/renderro/62b0ccfb-6d6c-4fff-81fa-30a27ed90333', '62b0ccfb-6d6c-4fff-81fa-30a27ed90333').zip()