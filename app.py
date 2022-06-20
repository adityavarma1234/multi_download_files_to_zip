import ast, os
from flask import Flask, redirect, url_for, request, render_template, jsonify, send_file
from multiprocessing import Process, Manager

from url_downloader import UrlDownloader
from status_values import StatusValues


app = Flask(__name__)
global_status_hash = Manager().dict()

def process_url_download(url_downloader, global_status_hash):
	if(url_downloader.download(global_status_hash)):
		if(url_downloader.zip_files()):
			global_status_hash[url_downloader.uuid] = StatusValues.Completed.name
			print("updated_global_status hash ", global_status_hash)

@app.route('/success/<value>')
def success(value):
	return jsonify({'archive_hash': value})

@app.route('/failure/<value>')
def failure(value):
	return jsonify({'error': 'incorrect value passed'})


@app.route('/api/archive/create', methods= ['POST', 'GET'])
def create():
	if request.method == 'POST':
		urls = request.form['urls']
		print("urls type is ", type(urls))
		print("Urls fetched are :", urls)
		url_downloader = UrlDownloader(ast.literal_eval(urls))
		uuid = url_downloader.uuid
		# global_status.add(uuid, StatusValues.InProgress.name)
		global_status_hash[uuid] = StatusValues.InProgress.name
		process = Process(target = process_url_download, args=(url_downloader, global_status_hash))
		process.start()

		# url_downloader.download()
		return redirect(url_for('success', value = uuid))
	else:
		return render_template("create.html")

def generate_get_uuid_url(uuid):
	# TODO: Replace with string formatter and add test cases
	return "http://localhost/archive/get/" + uuid + '.zip'

@app.route('/api/archive/status/<uuid>', methods= ['GET'])
def archive_status(uuid):
	print("fetching global_status hash ", global_status_hash)
	if uuid in global_status_hash:
		if global_status_hash[uuid] == StatusValues.Completed.name:
			status = global_status_hash[uuid]
			url = generate_get_uuid_url(uuid)
			return jsonify({'status': status, 'url': url})
		else:
			status = global_status_hash[uuid]
			return jsonify({'status': status})
	else:
		return jsonify({'error': 'Invalid uuid'})

@app.route('/archive/get/<filename>', methods= ['GET'])
def download_zip(filename):
	zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zip_data', filename)
	if not os.path.exists(zip_file_path):
		return jsonify({'error': 'Invalid zip file passed'})
	else:
		return send_file(zip_file_path, mimetype='zip', attachment_filename=filename, as_attachment=True)

if __name__ == "__main__":
	# global_status = StatusHelper() 
	global_status_hash = Manager().dict()
	app.run(debug = True)
