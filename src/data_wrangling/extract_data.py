from argparse import ArgumentParser
import json
from os import makedirs, remove
from os.path import join, isdir
from abc import ABC, abstractmethod

import openreview
from pdfminer.high_level import extract_text

from OpenReviewLabRotation.src.config import METAREVIEW, ETHICSREVIEW, COMMENT, REVIEW, PAPER, WITHDRAWALCONF

ABSTRACT = "abstract"
NO_UNKNOWN = "no_unknown_note_type"


class ConferenceLike(ABC):
    """
    Define a ConferenceLike subclass for each conference, workshop etc. from which you want to extract data.
    Make sure to define def get_note_type.
    """
    @abstractmethod
    def __init__(self, client, invitation_id):
        self.client = client
        self.invitation_id = invitation_id

    @abstractmethod
    def get_note_type(self, content: dict) -> str:
        """ Define what note type the note is. If a note type isn't known, return empty string.
        Examples of note types: review, metareview, comment, etc.

        :param content:
        :return: Return the note type of the Note (e.g. review, metareview, comment, etc.) or empty string if unknown
        """
        pass

    def get_forum(self, subm_id: str) -> dict:
        """

        :param subm_id: id of submission of which data gets extracted.
        :return: forum_dict containing things like reviews, comments, meta data, etc. of the subm_id
        """
        forum_dict = {}
        # Get representation of forum of a submission. E.g. https://openreview.net/forum?id=SkgkJn05YX is a forum.
        forum = self.client.get_notes(forum=subm_id)
        note_type_count = {}
        no_unknown = True
        for note in forum:
            content = note.content
            note_type = ""
            note_type = self.get_note_type(content)
            # TODO: Also include a "SKIP" string for when a note should be skipped (e.g. withdrawal submission)
            # note and skip if unknown note type
            if not note_type:
                print("Unknown note type for " + str(subm_id) +  "! Note type candidates were: " + str(content.keys()))
                no_unknown = False
                continue

            # save note content
            forum_dict[note_type + "_" + str(note_type_count.get(note_type, 0))] = content
            # increment note_type counter
            note_type_count[note_type] = note_type_count.get(note_type, 0) + 1
        # Mark if there were unknown note types or not. data_stats.py will show in the result dictionary
        if no_unknown:
            forum_dict[NO_UNKNOWN] = True
        return forum_dict

    def get_pdf_str(self, subm_id: str) -> str:
        """

        :param subm_id: id of submission of which the pdf gets extracted.
        :return: pdf of subm_id as string
        """
        TEMP_PDF = "temp.pdf"
        binary_pdf = self.client.get_pdf(subm_id)
        # FIXME: It's really ugly to have to write the binary_pdf to a file first.
        with open(TEMP_PDF, 'wb') as op:
            op.write(binary_pdf)
        pdf_str = extract_text(TEMP_PDF)
        remove(TEMP_PDF)
        return pdf_str


class ICLR2013Conference(ConferenceLike):
    """
    * Metareview doesn't give a review score, but says for what the paper was accepted.
    * Normal reviews only consist of title and text
    TODO:
    * reviews and comments are not differentiated
    * PDFs aren't getting extracted. Presumably because pdf link doesn't point to pdf (it points to arxiv)
    """

    def __init__(self, client):
        super().__init__(client, "ICLR.cc/2013/conference/-/submission")

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == "decision":
                return METAREVIEW
            elif key == ABSTRACT:
                return PAPER
            elif key == REVIEW:
                return REVIEW
        keys = content.keys()
        if COMMENT in keys or "reply" in keys:
            return COMMENT
        return ""


class ICLR2014Conference(ConferenceLike):
    """
    * Normal reviews only consist of title and text
    TODO
    * A lot of paper have as decision "decision": "submitted, no decision". Haven't checked if there are any with a different value
    """

    def __init__(self, client):
        super().__init__(client, "ICLR.cc/2014/conference/-/submission")


    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == "decision":
                return METAREVIEW
            elif key == ABSTRACT:
                return PAPER
            elif key == REVIEW:
                return REVIEW
        keys = content.keys()
        if COMMENT in keys or "reply" in keys:
            return COMMENT
        return ""


class ICLR2017Conference(ConferenceLike):
    """
    * Metareview doesn't give a review score, but says for what the paper was accepted. (differently than ICLR 2013 though).
      Maybe some give a review score in the comment
    * Normal reviews give confidence and rating
    TODO
    * 3 non-extracted PDFs
    """

    def __init__(self, client):
        super().__init__(client, "ICLR.cc/2017/conference/-/submission")

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == "decision":
                return METAREVIEW
            elif key == ABSTRACT:
                return PAPER
            elif key == REVIEW:
                return REVIEW
        keys = content.keys()
        if COMMENT in keys or "question" in keys or list(keys) == ["title"]:
            return COMMENT
        return ""


class ICLR2018Conference(ConferenceLike):
    """
    * Metareview usually doesn't give a review score, but says for what the paper was accepted (like 2017).
      Some metareviews also have scores in the comment text though (see submission B1ae1lZRb).
    * Normal Review: Like ICLR 2017
    TODO
    * 2 non-extracted PDFs
    """

    def __init__(self, client):
        super().__init__(client, "ICLR.cc/2018/Conference/-/Blind_Submission")

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == "decision":
                return METAREVIEW
            elif key == ABSTRACT:
                return PAPER
            elif key == REVIEW:
                return REVIEW
        if COMMENT in content.keys():
            return COMMENT
        return ""


class ICLR2019Conference(ConferenceLike):
    """
    * Metareview has a numerical confidence score and for what the paper was accepted (like 2017).
    * Normal Review: Like ICLR 2017
    TODO
    * 3 non-extracted PDFs
    """

    def __init__(self, client, invitation_id="ICLR.cc/2019/Conference/-/Blind_Submission"):
        self.NOTE_TYPES_IDS = {ABSTRACT, METAREVIEW, COMMENT, REVIEW, WITHDRAWALCONF}
        super().__init__(client, invitation_id)

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key in self.NOTE_TYPES_IDS:
                note_type = key
                if key == ABSTRACT:
                    note_type = PAPER
                return note_type
        return ""


class ICLR2020Conference(ICLR2019Conference):
    """
    * Metareview: Like ICLR 2017
    TODO
    * Normal Review: Gives rating score, but no confidence. Also has additional textual comments that haven't been seen before
    * 1 non-extracted PDF
    """

    def __init__(self, client):
        super().__init__(client, "ICLR.cc/2020/Conference/-/Blind_Submission")


class ICLR2021Conference(ConferenceLike):
    """
    * Normal Review: Like ICLR 2017
    """

    def __init__(self, client):
        self.OFFICIAL_REVIEW = "Official Review of Paper"
        super().__init__(client, "ICLR.cc/2021/Conference/-/Blind_Submission")

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == ABSTRACT:
                return PAPER
            elif key == REVIEW:
                return REVIEW
        if ETHICSREVIEW in content.keys():
            return ETHICSREVIEW
        elif "decision" in content.keys():
            return METAREVIEW
        elif COMMENT in content.keys():
            return COMMENT
        return ""


class ICLR2022Conference(ConferenceLike):
    """
    * Metareview: Like ICLR 2017
    * Review: Main score is the "recommendation" score. Also has other scores about more fine-grained aspects of the reviewed submission
    """

    def __init__(self, client):
        self.OFFICIAL_REVIEW = "Official Review of Paper"
        super().__init__(client, "ICLR.cc/2022/Conference/-/Blind_Submission")

    def get_note_type(self, content: dict) -> str:
        for key in content.keys():
            if key == "decision":
                return METAREVIEW
            elif key == "main_review":
                return REVIEW
            elif key == ABSTRACT:
                return PAPER
        # only check after checking other keys since a lot of other note types have comments
        if COMMENT in content.keys():
            return COMMENT
        return ""


def maybe_create_dir(dir_name: str) -> None:
    if not isdir(dir_name):
        makedirs(dir_name, exist_ok=True)


def extract_subm_data(subm_id, conf_obj, save_dir):
    """ Extract the data for a submission

    :param subm_id: id of the submission to extract data from.
    :param conf_obj: Object for the Conference or Workshop in question
    :param save_dir: Where the data gets saved
    :return: if an unknown note type was encountered or pdf couldn't get extracted
    """
    # collect data in subm_dict
    subm_dict = {}

    # Track if unknown note type or sth. with pdf went wrong
    unknown_note = False
    no_pdf = False

    subm_dict = conf_obj.get_forum(subm_id)
    if not NO_UNKNOWN in subm_dict.keys():
        unknown = True

    try:
        subm_dict["pdf"] = conf_obj.get_pdf_str(subm_id)
    except Exception:
        no_pdf = True

    # Save data
    with open(join(save_dir, str(subm_id) + ".json"), "w") as outfile:
        json.dump(subm_dict, outfile, sort_keys=True, indent=4)


def main(invitation: str, data_root_dir: str, data_parent_dir: str, client: openreview.Client, conference_like: str, skip_past: str) -> None:
    """ Save data of papers of the invitation id as .json files

    :param invitation: Invitation Id for Submissions. See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
    :param data_root_dir: Directory where data gets saved
    :param client: An openreview.Client object. Some submissions are only visible with certain rights, I assume.
    :param conference_like: The name of the corresponding ConferenceLike class.
    :param skip_past: Extract data of only the submissions coming after the provided submission id
    """
    save_dir = join(data_root_dir, invitation, data_parent_dir)
    maybe_create_dir(save_dir)

    conf_obj = eval(conference_like)(client)

    submission_iterator = openreview.tools.iterget_notes(client, invitation=invitation)
    skip = bool(skip_past)

    for submission in submission_iterator:
        subm_id = submission.id
        if skip:
            if subm_id == skip_past:
                skip = False
            continue
        print(subm_id)
        extract_subm_data(subm_id, conf_obj, save_dir)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--invitation", type=str,
                        help="Invitation Id for Submissions. "
                             "See https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions",
                        default='ICLR.cc/2019/Conference/-/Blind_Submission')
    parser.add_argument("--data_root_dir", type=str, help="Root directory where data gets saved", default="../../data/")
    parser.add_argument("--data_parent_dir", type=str, help="Parent directory where data gets saved", default="submission_dicts")
    parser.add_argument("--conference_like", type=str, help="The name of the corresponding Conference class. Each "
                                                             "conference-like object needs a Conference class",
                        default="ICLR2019Conference")
    parser.add_argument("--skip_past", type=str, help="Extract data of only the submissions coming after the provided submission id.", default="")
    arg_dict = vars(parser.parse_args())
    client = openreview.Client(baseurl='https://api.openreview.net')
    arg_dict["client"] = client
    main(**arg_dict)
