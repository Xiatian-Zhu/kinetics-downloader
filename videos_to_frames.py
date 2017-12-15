import argparse, json

import lib.config as config
import lib.parallel_to_frames as parallel

def process_category(category, num_workers, failed_save_file):

  with open(config.CATEGORIES_PATH, "r") as file:
    categories = json.load(file)

  if category not in categories:
    raise ValueError("Category {} not found.".format(category))

  classes = categories[category]
  process_classes(classes, num_workers, failed_save_file)

def process_classes(classes, num_workers, failed_save_file):

  for source_root, target_root in zip([config.TRAIN_ROOT, config.VALID_ROOT],
                                        [config.TRAIN_FRAMES_ROOT, config.VALID_FRAMES_ROOT]):

    pool = parallel.Pool(classes, source_root, target_root, num_workers, failed_save_file)
    pool.start_workers()
    pool.feed_videos()
    pool.stop_workers()

def main(args):

  if args.all:
    with open(config.CATEGORIES_PATH, "r") as file:
      categories = json.load(file)

    for category in categories:
      process_category(category, args.num_workers, args.failed_log)

  else:
    if args.categories:
      for category in args.categories:
        process_category(category, args.num_workers, args.failed_log)

    if args.classes:
      process_classes(args.classes, args.num_workers, args.failed_log)

    if args.json_classes:
      with open(args.json_classes, "r") as file:
        classes = json.load(file)

      process_classes(classes, args.num_workers, args.failed_log)

    if args.test:
      with open(config.TEST_METADATA_PATH) as file:
        data = json.load(file)

      pool = parallel.Pool(None, config.TEST_ROOT, config.TEST_FRAMES_ROOT, args.num_workers, args.failed_log)
      pool.start_workers()
      pool.feed_videos()
      pool.stop_workers()

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--categories", nargs="+", help="categories to download")
  parser.add_argument("--classes", nargs="+", help="classes to download")
  parser.add_argument("--all", action="store_true", help="download the whole dataset")
  parser.add_argument("--json-classes", help="path to a JSON file with a list of classes")
  parser.add_argument("--test", action="store_true", help="download the test set")

  parser.add_argument("--num-workers", type=int, default=1)
  parser.add_argument("--failed-log", default="dataset/failed_frames.txt", help="where to save list of failed videos")

  parsed = parser.parse_args()
  main(parsed)
