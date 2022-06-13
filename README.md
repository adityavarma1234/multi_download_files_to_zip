# multi_download_files_to_zip
Download multiple files and convert to zip


Running steps

1. Pull image aditya1234/python_flask_multi_downloader_to_zip
2. Run image by using the command `docker run -d -p 5000:5000 <>`
3. If facing issues with port change the first 5000 to another value.



Testing steps

1. Go to http://localhost:5000/api/archive/create and provide list of urls for testing. Sample urls [
'https://www.northwestknowledge.net/metdata/data/pr_1979.nc',
 'https://www.northwestknowledge.net/metdata/data/pr_1980.nc'
]
2. Make sure that there is no trailing white space when providing the input. 
3. Click on create. 
4. If it is successful you will be redirected to `http://localhost:5000/success/<uuid>` page
5. Go to `http://localhost:5000/api/archive/status/<uuid>` to check the current status
6. Once the status is completed go to `localhost:5000/archive/get/<uuid.zip>` to fetch the file