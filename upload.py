import os
# from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from GisApi import UPLOAD_FOLDER


def upload_file():
    print os.curdir(__file__)
    print "file uploaded"



    # def post(self):
	# 	parse = reqparse.RequestParser()
	# 	parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
	# 	args = parse.parse_args()
	# 	gis_file = args['file']
	# 	file_name = secure_filename(gis_file.filename)
	# 	path = os.path.join(app.config['UPLOAD_FOLDER'],file_name)
	# 	gis_file.save("{}".format(path))
	# 	return 'OK', 200
