import re
from json import dump, load, JSONEncoder
from os import listdir
from os.path import join, dirname
from argparse import ArgumentParser

from matplotlib import pyplot as plt
from transformers import AutoTokenizer
from numpy import arange

from OpenReviewLabRotation.src.config import PDF


def main(data_dir_list, tokenizer_and_ids):

    tokenizer = tokenizer_and_ids[0]
    input_ids = tokenizer_and_ids[1]
    token_lengths = []
    for data_dir in data_dir_list:
        file_names = listdir(data_dir)
        for file_name in file_names:
            with open(join(data_dir, file_name), 'r') as f:
                subm_dict = load(f)
                try:
                    pdf_text = subm_dict[PDF]
                    token_lengths.append(len(tokenizer(pdf_text)[input_ids]))
                except KeyError:
                    pass

    plt.hist(token_lengths, bins="auto")
    plt.xticks(arange(0, 100000, 10000))
    plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
#     example content for content of such a text file:
#     ["/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2022/Conference/-/Blind_Submission/submission_dicts",
# "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2021/Conference/-/Blind_Submission/submission_dicts",
# "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2020/Conference/-/Blind_Submission/submission_dicts",
# "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2019/Conference/-/Blind_Submission/submission_dicts",
# "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2018/Conference/-/Blind_Submission/submission_dicts",
# "/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2017/conference/-/submission/submission_dicts"]
    parser.add_argument("--data_dir_list", type=str, help="Text file containing list of directories where data to summarize lie",
                        default="cross_inv.txt")
    data_dir_list_file = vars(parser.parse_args())["data_dir_list"]
    data_dir_list = []
    with open(data_dir_list_file, "r") as f:
        data_dir_list = eval(f.read())
    # TODO: Maybe allow user to specify other tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
    tokenizer_and_ids = (tokenizer, "input_ids")
    main(data_dir_list, tokenizer_and_ids)
