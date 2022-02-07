# TODO: Iterate through json files
# TODO: Count the number of comments, reviews, papers, metareviews
# TODO: Count how many papers are missing
# TODO: Replace directory with parse arg.

import re
from json import dump, load, JSONEncoder
from os import listdir
from os.path import join, dirname
from pathlib import Path
from argparse import ArgumentParser

from OpenReviewLabRotation.src.config import COMMENT, METAREVIEW, ETHICSREVIEW, WITHDRAWALCONF


class SetEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
            return JSONEncoder.default(self, obj)


def pure_key(key):
    """ If key is e.g. 'comment_12', return value is 'comment' """
    return re.split("_\d+", key)[0]


def get_submid(file_name):
    return file_name[:-len(".json")]



def main(data_dir, dump_dir, skip_keys):

    COUNTER = "_counter"

    stat_dict = {}
    file_names = listdir(data_dir)
    too_many_metarevs = []

    # collect all available keys and how often they occur
    for file_name in file_names:
        with open(join(data_dir, file_name), 'r') as f:
            subm_dict = load(f)
            for key in subm_dict.keys():
                subm_key = pure_key(key)
                stat_key = subm_key + COUNTER
                stat_dict[stat_key]= stat_dict.get(stat_key, 0) + 1
                if key == METAREVIEW + "_1":
                    # if a submission has more than one meta review, note it
                    too_many_metarevs.append(get_submid(file_name))

    ALL_KEYS = set([key[:-len(COUNTER)] for key in stat_dict.keys()])

    stat_dict["submission_counter"] = len(file_names)
    stat_dict["too_many_metareviews"] = too_many_metarevs


    missed_keys_dict = {}
    skip_keys = set(skip_keys)

    # collect what submissions didn't have what keys
    for file_name in file_names:
        with open(join(data_dir, file_name), 'r') as f:
            subm_dict = load(f)
            subm_keys = [pure_key(key) for key in subm_dict.keys()]
            missed_keys = ALL_KEYS.difference(subm_keys)
            # It's fine if keys from skip_keys are missing (e.g. comments)
            missed_keys = missed_keys.difference(skip_keys)

            if missed_keys:
                missed_keys_dict[get_submid(file_name)] = missed_keys

    stat_dict["missed_keys"] = missed_keys_dict
    stat_dict["missed_key_counter"] = len(missed_keys_dict)

    # save the file
    out_path = join(dirname(data_dir), dump_dir + ".json")

    with open(out_path, "w") as out_file:
        dump(stat_dict, out_file, sort_keys=True, indent=4, cls=SetEncoder)
          
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="Directory where data to summarize lies",
                        default="../../data/ICLR.cc/2019/Conference/-/Blind_Submission/submission_dicts")
    parser.add_argument("--dump_dir", type=str, help="What the stat dictionary should be called", default="stat_dict.json")
    # TODO: Rename and description
    parser.add_argument("--skip_keys", type=str, nargs="*", default=[COMMENT, ETHICSREVIEW, WITHDRAWALCONF])
    arg_dict = vars(parser.parse_args())
    main(**arg_dict)
