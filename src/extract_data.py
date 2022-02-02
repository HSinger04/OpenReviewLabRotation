from argparse import ArgumentParser
import json
from os import makedirs, remove
from os.path import join, isdir

import openreview
from pdfminer.high_level import extract_text


ABSTRACT = "abstract"
NOTE_TYPES = {ABSTRACT, "metareview", "comment", "review"}


def maybe_create_dir(dir_name: str) -> None:
    if not isdir(dir_name):
        makedirs(dir_name, exist_ok=True)


def get_forum(subm_id: str) -> dict:
    """

    :param subm_id: id of submission of which data gets extracted.
    :return: dict containing things like reviews, comments, meta data, etc. of the subm_id
    """
    forum_dict = {}
    # Get representation of forum of a submission. E.g. https://openreview.net/forum?id=SkgkJn05YX is a forum.
    forum = client.get_notes(forum=subm_id)
    note_type_count = dict.fromkeys(NOTE_TYPES, 0)
    for note in forum:
        content = note.content
        for key in content.keys():
            if key in NOTE_TYPES:
                save_key = key
                if key == ABSTRACT:
                    save_key = "paper"
                # FIXME: Saving the numbers rn is ugly, since e.g. 11 < 2 in terms of string sort
                save_key += "_" + str(note_type_count[key])
                forum_dict[save_key] = content
                note_type_count[key] += 1
                break
        else:
            raise RuntimeError("Unknown note type! Note type candidates were: " + str(content.keys()))

    return forum_dict


def get_pdf_str(subm_id: str) -> str:
    """

    :param subm_id: id of submission of which the pdf gets extracted.
    :return: pdf of subm_id as string
    """
    TEMP_PDF = "temp.pdf"
    binary_pdf = client.get_pdf(subm_id)
    # FIXME: It's really ugly to have to write the binary_pdf to a file first.
    with open(TEMP_PDF, 'wb') as op:
        op.write(binary_pdf)
    pdf_str = extract_text(TEMP_PDF)
    remove(TEMP_PDF)
    return pdf_str


def main(invitation: str, data_dir: str, client: openreview.Client) -> None:
    """

    :param invitation: Invitation Id for Submissions. See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
    :param data_dir: Directory where data gets saved
    :param client: An openreview.Client object
    """
    save_dir = join(data_dir, invitation)
    maybe_create_dir(save_dir)

    submission_iterator = openreview.tools.iterget_notes(client, invitation=invitation)
    for submission in submission_iterator:
        subm_id = submission.id

        # collect data in note_dict
        note_dict = get_forum(subm_id)
        note_dict["pdf"] = get_pdf_str(subm_id)

        # Save data
        with open(join(save_dir, str(subm_id) + ".json"), "w") as outfile:
            json.dump(note_dict, outfile, sort_keys=True, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--invitation", type=str,
                        help="Invitation Id for Submissions. "
                             "See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions",
                        default='ICLR.cc/2019/Conference/-/Blind_Submission')
    parser.add_argument("--data_dir", type=str, help="Directory where data gets saved", default="../data/")
    arg_dict = vars(parser.parse_args())
    client = openreview.Client(baseurl='https://api.openreview.net')
    arg_dict["client"] = client
    main(**arg_dict)