import os
import json
import glob
from classify.classifier2 import babadook

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
#PARENT_DIR = os.path.abspath(os.path.join(CUR_DIR, os.pardir))
#DATA_DIR = os.path.join(PARENT_DIR, "input")
#IMAGE_DIR = os.path.join(DATA_DIR, "image")
DATA_DIR = os.path.join(CUR_DIR, "test_dataset")
IMAGE_DIR = os.path.join(DATA_DIR)

def predict_label(json_data, filename):
	drivename, fname = filename.split("/")
	df = drivename + '_' + fname
	fname = fname.split(".")[0]
	bounding_box_path = os.path.join("classify/bounding_boxes",(df +'.json'))
	bounding_box_filename = os.path.join(CUR_DIR, bounding_box_path)
	output_path = os.path.join(CUR_DIR, "classify/write_data.txt")
	image_filename = os.path.join(DATA_DIR, drivename, "image", fname+'.png')

	images_to_delete = os.path.join(CUR_DIR, "classify/inception/*jpg")
	all_files = glob.glob(images_to_delete)
	for f in all_files:
		os.remove(f)

	#json_data = json.dumps(json_data)

	try:
		open(bounding_box_filename, 'w').close()
	except Exception as e:
		pass
	with open(bounding_box_filename,'a') as f:
		f.write(json_data)
#	os.system("python3 {} --image_file={}".format(os.path.join(CUR_DIR, "classify/classifier.py"), image_filename))
	babadook(df)
	folder_to_empty = os.path.join(CUR_DIR, "classify/bounding_boxes/*json")
	files = glob.glob(folder_to_empty)
	for f in files:
		os.remove(f)
	#data = os.popen("cat {}".format(output_path)).read()
	f = open(output_path, "r")
	data = f.readlines()

	os.system("rd classify/bounding_boxes/*.json")
	hi = ''
	l = open(os.path.join(CUR_DIR, 'keywords.txt'), "w")
	#return get_keyword(data)
	for x in data:
		hi = get_keyword(x)
		l.write(str(hi) + '\n')
	f.close()
	l.close()
	return hi

def get_keyword(data):
	pedestrian_keywords = {'person', 'man', 'woman', 'walker', 'pedestrian'}
	car_keywords = {'car'}
	van_keywords = {'van', 'minivan', 'bus', 'minibus'}
	truck_keywords = {'truck'}
	cyclist_keywords = {'cyclist', 'motorcyclist', 'unicyclist', 'bicycle', 'motocycle', 
						'bike', 'motorbike', 'unicycle', 'monocycle', 'rickshaw'}

	words = []
	for w in data.split(','):
		words.extend(w.split(' '))
	words = set(words)
	if words.intersection(car_keywords):
		return	'car'
	if words.intersection(van_keywords):
		return 'van'
	if words.intersection(truck_keywords):
		return 'truck'
	if words.intersection(pedestrian_keywords):
		return 'pedestrian'
	if words.intersection(cyclist_keywords):
		return 'cyclist'
	return -1


# filenamee = '8_drive_0004_sync/0000000007'
# with open(r'C:\Rabeea\UNI\STUDY\fyp\latte\app\classify\bounding_boxes/0000000007.json') as f:
#   json_dataa = json.load(f)
#
# ello = predict_label(json_dataa, filenamee)
# print(ello)