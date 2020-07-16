import json
import os
import random


TAL_videos_dict = {}

# random.seed(0)

list_path = 'resources/kinetics600/validate.json'
with open(list_path) as file:
    videos_dict = json.load(file)

    with open('resources/srib_categories.json', "r") as file:
        categories = json.load(file)

    for cat in categories:
        print(cat)
        act_classes = categories[cat]
        print(act_classes)

        video_num_per_class = int(max(4, 10 / len(act_classes)))
        
        for class_name in act_classes:
            print(class_name)
            ori_class_name = class_name.replace("_", " ")
            # class_dir = os.path.join(cat, class_name.replace(" ", "_"))
            # if not os.path.isdir(class_dir):
            #     # when using multiple processes, the folder might have been already created (after the if was evaluated)
            #     try:
            #         os.mkdir(class_dir)
            #     except FileExistsError:
            #         pass
            
            # Iterate all videos for an action class
            video_num_per_class_counter = 0
            for key in videos_dict.keys():
                metadata = videos_dict[key]
                annotations = metadata["annotations"]

                if annotations["label"].lower() == ori_class_name.lower():
                    video_num_per_class_counter += 1
                    TAL_videos_dict[key] = metadata

                    clip_start = annotations["segment"][0]
                    clip_end = annotations["segment"][1]

                    # Extends at two ends, at least 30 seconds extended
                    start_ext = min(clip_start, random.randint(5, 25))
                    end_ext = random.randint(30-start_ext, 30-start_ext+20)
                    annotations["extends"] = [float(start_ext), float(end_ext)]
    
                if video_num_per_class_counter >= video_num_per_class:
                    print("Extend the class: {} done".format(class_name))
                    break

    print("\n*** Video selected ****: {}\n".format(len(TAL_videos_dict)))

    with open('srib_val.json', 'w') as of:
        json.dump(TAL_videos_dict, of)

