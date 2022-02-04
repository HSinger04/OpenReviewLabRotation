from argparse import ArgumentParser
import json
from os import makedirs, remove
from os.path import join, isdir
from abc import ABC, abstractmethod

import openreview
from pdfminer.high_level import extract_text


class ConferenceLike(ABC):
    """
    Define a ConferenceLike subclass for each conference, workshop etc. from which you want to extract data.
    Make sure to define def get_note_type.
    """

    @abstractmethod
    def get_note_type(self, content: openreview.Note) -> str:
        """ Define what note type the note is (if at all). Examples of note types: review, metareview, comment, etc.

        :param content:
        :return: Return the note type of the Note (e.g. review, metareview, comment, etc.)
        """
        pass

    def get_forum(self, subm_id: str) -> dict:
        """

        :param subm_id: id of submission of which data gets extracted.
        :return: forum_dict containing things like reviews, comments, meta data, etc. of the subm_id
        """
        forum_dict = {}
        # Get representation of forum of a submission. E.g. https://openreview.net/forum?id=SkgkJn05YX is a forum.
        forum = client.get_notes(forum=subm_id)
        note_type_count = {}
        for note in forum:
            content = note.content
            note_type = self.get_note_type(content)
            if not note_type:
               raise RuntimeError("Unknown note type! Note type candidates were: " + str(content.keys()))

            # save note content
            forum_dict[note_type + "_" + str(note_type_count.get(note_type, 0))] = content
            # increment note_type counter
            note_type_count[note_type] = note_type_count.get(note_type, 0) + 1
        return forum_dict

    def get_pdf_str(self, subm_id: str) -> str:
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


class ICLR2019Conference(ConferenceLike):

    def __init__(self):
        self.ABSTRACT = "abstract"
        self.NOTE_TYPES = {self.ABSTRACT, "metareview", "comment", "review"}
        super(ConferenceLike, self).__init__()

    def get_note_type(self, content: openreview.Note) -> str:
        for key in content.keys():
            if key in self.NOTE_TYPES:
                note_type = key
                if key == self.ABSTRACT:
                    note_type = "paper"
                # FIXME: Saving the numbers rn is ugly, since e.g. 11 < 2 in terms of string sort
                return note_type
        return ""


def maybe_create_dir(dir_name: str) -> None:
    if not isdir(dir_name):
        makedirs(dir_name, exist_ok=True)


def main(invitation: str, data_dir: str, client: openreview.Client, conference_class: str) -> None:
    """ Save data of papers of the invitation id as .json files

    :param invitation: Invitation Id for Submissions. See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
    :param data_dir: Directory where data gets saved
    :param client: An openreview.Client object
    :param conference_class: The name of the corresponding Conference class.
    """
    save_dir = join(data_dir, invitation)
    maybe_create_dir(save_dir)

    conf_obj = eval(conference_class)()

    submission_iterator = openreview.tools.iterget_notes(client, invitation=invitation)
    for submission in submission_iterator:
        subm_id = submission.id

        # collect data in note_dict
        forum_dict = conf_obj.get_forum(subm_id)
        forum_dict["pdf"] = conf_obj.get_pdf_str(subm_id)

        # Save data
        with open(join(save_dir, str(subm_id) + ".json"), "w") as outfile:
            json.dump(forum_dict, outfile, sort_keys=True, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--invitation", type=str,
                        help="Invitation Id for Submissions. "
                             "See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions",
                        default='ICLR.cc/2019/Conference/-/Blind_Submission')
    parser.add_argument("--data_dir", type=str, help="Directory where data gets saved", default="../data/")
    parser.add_argument("--conference_class", type=str, help="The name of the corresponding Conference class. Each "
                                                             "conference-like object needs a Conference class",
                        default="ICLR2019Conference")
    arg_dict = vars(parser.parse_args())
    client = openreview.Client(baseurl='https://api.openreview.net')
    arg_dict["client"] = client
    main(**arg_dict)
