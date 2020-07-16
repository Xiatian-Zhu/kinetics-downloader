import json
import os
import random
import lib.downloader as dl

failed_videos = []

video_save_dir = 'dataset/srib/'
if not os.path.isdir(video_save_dir):
    try:
        os.mkdir(video_save_dir)
    except FileExistsError:
        pass

meta_file_path = 'resources/srib_val.json'
with open(meta_file_path) as file:
    videos_dict = json.load(file)

    with open('resources/srib_categories.json', "r") as file:
        categories = json.load(file)

    for cat in categories:
        print(cat)
        cat_dir = os.path.join(video_save_dir, cat)
        if not os.path.isdir(cat_dir):
            try:
                os.mkdir(cat_dir)
            except FileExistsError:
                pass

        act_classes = categories[cat]
        print(act_classes)

        video_num_per_class = int(max(4, 10 / len(act_classes)))
        
        for class_name in act_classes:
            print(class_name)
            ori_class_name = class_name.replace("_", " ")
            class_dir = os.path.join(video_save_dir, cat, class_name.replace(" ", "_"))
            if not os.path.isdir(class_dir):
                # when using multiple processes, the folder might have been already created (after the if was evaluated)
                try:
                    os.mkdir(class_dir)
                except FileExistsError:
                    pass
            
            # Iterately download all videos for an action class
            for key in videos_dict.keys():
                metadata = videos_dict[key]
                annotations = metadata["annotations"]

                if annotations["label"].lower() == ori_class_name.lower():

                    clip_start = annotations["segment"][0]
                    clip_end = annotations["segment"][1]

                    # Extends at two ends
                    ext_start = annotations["extends"][0]
                    ext_end = annotations["extends"][1]

                    start = clip_start - ext_start
                    end = clip_end + ext_end

                    # To download this tal video clip
                    if not dl.process_video(key, class_dir, start, end):
                        failed_videos.append(key)
    

