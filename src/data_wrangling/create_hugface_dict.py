from os import listdir
from os.path import dirname, join
from json import load, dump

from OpenReviewLabRotation.src.config import PDF, REVIEW

rev_length = len(REVIEW)


def get_hugface_dict(subm_dict: dict, extr_keys = [REVIEW]):
    """ TODO: Also returns review scores and make it useable for other ConferenceLikes except for ICLR 2022

    :param subm_dict: submission dict as extracted with extract_data.py
    :return: dict compatible for huggingface dataset creation
    """
    hugface_dicts = []

    if not PDF in subm_dict.keys():
        return []

    for key, value in subm_dict.items():
        if REVIEW == key[:rev_length]:
            hugface_dict = {}
            hugface_dict[PDF] = subm_dict[PDF]
            hugface_dict[REVIEW] = subm_dict[key]["main_review"]
            hugface_dicts.append(hugface_dict)
    return hugface_dicts


if __name__ == "__main__":
    # TODO: Change arguments to be able to be parsed from command line
    local_save_dir = "hugface_dicts"
    data_dir = "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2022/Conference/-/Blind_Submission/submission_dicts"
    file_names = listdir(data_dir)
    hugface_dicts = []
    for file_name in file_names:
        with open(join(data_dir, file_name), "r") as f_in:
            hugface_dicts += get_hugface_dict(load(f_in))

    dump_dict = {"data": hugface_dicts}
    save_file = join(dirname(data_dir), local_save_dir + ".json")
    with open(save_file, "w") as f_out:
        dump(dump_dict, f_out, sort_keys=True, indent=4)