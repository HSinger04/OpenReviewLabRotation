# OpenReviewLabRotation

## Explanation of project

The purpose of this lab rotation was to extract reviews from openreview.net and use that to train a model to generate review text and predict scores given a paper pdf as input.

## Examples

* [Example of extracted data](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/SkgkJn05YX.json)

## How-TOs

### Extracting Data

All the data extraction logic is contained in [extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py).
To extract data, run [extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py) as __main__. Make sure to take a look at what arguments the ArgumentParser takes.
After extracting data, make sure to run [submission data statistics](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/subm_stats.py) and check them. 
[create_hugface_dict.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/create_hugface_dict.py) transforms dicts extracted with [extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py) 
in a format similiar to [SQuAD-it](https://github.com/crux82/squad-it#release-format) and can be 
loaded similar to how it's done in https://huggingface.co/course/chapter5/2?fw=pt#loading-a-local-dataset.

#### OpenReview Python Client

Definitely check out the [OpenReview Python Client](https://openreview-py.readthedocs.io/en/latest/), as it gets used. 
The documentation is short and easy to read, so no worries. 

Especially https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
 is interesting for finding ids of conferences, workshops, etc. to extract data from them.

#### Information of specific conferences and workshops

To see for what conferences and workshops classes have already been implemented, see the subclasses
of ConferenceLike in "[extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py)". Make sure to especially read their doc string.
There, under TODO, bugs are also documented.

#### Extracting data from an unsupported conference or workshop

To see from what invitation ids the extracting data is supported, see "invitation_id" of the classes in "[extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py)".

To extract data from an unsupported conference or workshop, you need to implement a 
subclass of ConferenceLike and its abstract method get_note_type. One sees that a forum consists
of multiple Note objects, which can be reviews, comments, etc.:

<div align="center">
  <img src="https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/forum_and_notes.png">
</div>

The purpose of get_note_type is
to return based on the content of a Note (see the 'content' key-value pairs in above image)
the note type as a string. To see a list of available or add new note types, please use config.py

#### Data statistics

To get statistics across different conferences or workshops, use [cross_invitation_stats.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/cross_invitation_stats.py).
For statistics on a single conference or workshop, use [extract_data.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/extract_data.py) and potentially read https://github.com/HSinger04/OpenReviewLabRotation#extracting-data for more info.

## TODOs

* As the purpose of this lab rotation was to extract reviews from openreview.net and use that to train a model to generate review text and predict scores given a paper pdf as input, the following things need to still be done for that goal
  * Data preparation
    * While [create_hugface_dict.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/create_hugface_dict.py) already outputs something useful, it still has TODOs in it. See the TODO comments in the file.
    * [load_hugface_dicts.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/load_hugface_dicts.py) is an attempt at preparing a dataset from a dict extracted by [create_hugface_dict.py](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/src/data_wrangling/create_hugface_dict.py). However, the file in its current state is not useable, so it definitely needs to be worked on. The file content is more there to show what has been tried in the hopes that it helps whoever continues the work where I left off. 
    As any of the tokenized input pdf texts are too long to be fed into any transformer, the plan was to split the tokenized text into subparts such that each subparts can be fed
    into the encoder transformer of choice, the encodings would get summed together to represent the whole text and then get fed into the decoder. 
      * It might be helpful to look at https://colab.research.google.com/drive/1Ekd5pUeCX7VOrMx94_czTkwNtLN32Uyu?usp=sharing for an idea how to do this whole thing.
  * Model training
    * Nothing has been done for model training yet. A suggestion would be to use a transformer as an encoder that can take an input with as many tokens as possible (e.g. Longformer or [Infinite Memory Transformer](https://arxiv.org/abs/2109.00301) if an implementation exists later). For Decoder, one probably doesn't have to worry about limits on the output token length so much.
* Any TODO comments in any of the files.
