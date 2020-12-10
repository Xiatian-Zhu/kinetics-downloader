'''
 This file shows how to download the dataset videos using python
 For each video in the test set it
  - randomly scores frames
  - computes the average precision and nMSD
'''
__author__ = 'xzhu'

from os import listdir
from os.path import isfile, join, basename
import glob
import pdb

import pickle
import csv


def video_list(dirname, dataset_dir):

	exts = ['.webm', '.mp4', '.mkv', '.m4a']

	vfiles = []
	for ext in exts:
		vfiles = vfiles + glob.glob(dirname + '*' + ext)
	# 	cfiles = glob.glob('./*.csv')
		
	print('*** video files downloaded: {}'.format(len(vfiles)))

	vid_list = []
	for vd in vfiles:
		vf_name = basename(vd)
		vid = vf_name.split('.')[0]
		vid_list.append(vid)
		# print(vf_name, vid)

	vid_list = list(set(vid_list))
	print('*** video IDs downloaded: {}'.format(len(vid_list)))
	print('*** files - IDs: {}'.format(len(vfiles) - len(vid_list)))
	
	# -- Write a file
	f = open(dataset_dir + '_downloaded.txt', 'w')
	for vid in vid_list:
		f.write(vid+'\n')

	# # pdb.set_trace()
	# exist_vid = vfiles.copy()

	# for idx in range(len(vfiles)):
	# 	exist_vid[idx] = vfiles[idx][len(dirname):-4]
	# 	# vfiles[idx] = vfiles[idx][2:-4]
	
	# ################### Read all video IDs
	# all_vid = []

	# train_data_file = '/home/nfs/xiatian.zhu/codes/personalized-highlights-dataset/training.csv'
	# with open(train_data_file, newline='') as csvfile:
	# 	csv_reader = csv.reader(csvfile)
	# 	next(csv_reader)
	# 	for row in csv_reader:
	# 		all_vid.append(row[0])

	# all_vid = list(set(all_vid))
	# print('Total: {} videos'.format(len(all_vid)))

	# ############# Videos to be downloaded
	# nonexist_vid = list(set(all_vid) - set(exist_vid))
	# print('*** {} videos to be downloaded'.format(len(nonexist_vid)))

	# ################################################
	# # pdb.set_trace()
	# with open('train_videos_done', 'wb') as fp:
	# 	pickle.dump(exist_vid, fp)

	# # Write out a csv file
	# with open('PHD-GIFs_train_left.csv', 'w', newline='') as file:
	# 	writer = csv.writer(file)
	# 	# writer.writerows(nonexist_vid)
	# 	for item in nonexist_vid:
	# 		writer.writerow([item])

	# with open('PHD-GIFs_train_all.csv', 'w', newline='') as file:
	# 	writer = csv.writer(file)
	# 	# writer.writerows(nonexist_vid)
	# 	for item in all_vid:
	# 		writer.writerow([item])
	
	
# 	with open ('train_videos_done', 'rb') as fp:
# 		vlist = pickle.load(fp)
				
if __name__=='__main__':
	dataset_dir = 'Kinetics600_whole_videos'
	print(f'\no==> Dataset: {dataset_dir}\n')
	video_list('/home/nfs/datasets/' + dataset_dir + '/train/', dataset_dir)