"""
COnvert Kinetics annotation into the form of ActivityNet for 
temporal action localization.

An example of ActivityNet annotation
"v_QOlSCBRmfWY": {
        "duration_second": 82.730000000000004,
        "duration_frame": 2067,
        "annotations": [
            {
                "segment": [
                    6.195294851794072,
                    77.73085420904837
                ],
                "label": "Ballet"
            }
        ],
        "feature_frame": 2064
    }

"""

import json
import cv2
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip


def main():
    kinectis_annot_file = 'resources/srib_val_manual.json'
    video_dir = 'dataset/srib_manual_flatten/'
    output_annot_file = 'resources/srib-8_gt_anet_v2.json'

    output_dict = {}
    with open(kinectis_annot_file) as file:
        videos_dict = json.load(file)

        for idx, (k, v) in enumerate(videos_dict.items()):
            
            vid = k
            # vf = '/home/nfs/xiatian.zhu/codes/kinetics-downloader/dataset/srib_manual/clapping/clapping/1dfVFWG0ezo.mp4'
            vf = video_dir + vid + '.mp4'
            print('{}, {}'.format(idx, vf))

            cap = cv2.VideoCapture(vf)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            clip = VideoFileClip(vf)
            duration_second = clip.duration

            # if vid == '-7tDxxH2g6I':
            #     print(vid)

            annot = v["annotations"]
            new_annot = []
            annot_item = {}
            annot_item["segment"] = [annot['action'][0] - annot['segment'][0], annot['action'][1] - annot['segment'][0]]
            annot_item["label"] = annot['label']
            new_annot.append(annot_item)

            nv = {}
            nv['duration'] = duration_second
            nv['subset'] = 'validation'
            nv['duration_second'] = duration_second
            nv['duration_frame'] = frame_count
            nv['annotations'] = new_annot
            nv['feature_frame'] = 0
            nv['url'] = v['url']

            output_dict[k] = nv

    with open(output_annot_file, 'w') as outfile:
        json.dump(output_dict, outfile)


if __name__ == "__main__":
    main()