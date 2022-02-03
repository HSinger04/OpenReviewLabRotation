# TODO: Iterate through json files
# TODO: Count the number of comments, reviews, papers, metareviews
# TODO: Count how many papers are missing
# TODO: Replace directory with parse arg.

import re
from json import dump
from os import listdir
from os.path import join
from pathlib import Path

def main(data_dir, dump_dir):

    stat_dict = {}

    dirs = listdir(directory)
    for file in dirs:
        # TODO: Might have to specify full path or sth.
        with open(file, 'r') as f:
            datum = json.load(f)
            for key in datum.keys():
                # TODO: check what this returns
                stat_key = re.match("(.*?)_\d+", key).group()
                stat_dict.get(stat_key, 0) += 1

    stat_dict["num_submissions"] = len(dirs) 

    path = Path(data_dir)
    out_path = join(path.parent.absolute(), dump_dir + ".json") 

    # TODO: See if this works
    with open(out_path, "w") as out_file:
        dump(stat_dict, out_file, sort_keys=True, indent=4)
          
if __name__ == '__main__':
    arser = ArgumentParser()
    # TODO: default for data_dir
    parser.add_argument("--data_dir", type=str, help="Directory where data to summarize lies", default="../data/")
    parser.add_argument("--dump_dir", type=str, help="What the stat dictionary should be called", default="stat_dict") 
    arg_dict = vars(parser.parse_args())
    main(**arg_dict)
