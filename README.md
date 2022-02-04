# OpenReviewLabRotation

## Examples

* [Example of extracted data](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/SkgkJn05YX.json)

## How-TOs

### Extracting Data

All the data extraction logic is contained in extract_data.py.
To extract data, run extract_data.py as __main__. Make sure to take a look at what arguments the ArgumentParser takes.

#### OpenReview Python Client

Definitely check out the [OpenReview Python Client](https://openreview-py.readthedocs.io/en/latest/), as it gets used. 
The documentation is short and easy to read, so no worries. 

Especially https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
 is interesting for finding ids of conferences, workshops, etc. to extract data from them.



#### Extracting data from an unsupported conference or workshop

So far, getting the submissions from the following invitation ids are supported:

* ICLR.cc/2019/Conference/-/Blind_Submission

To extract data from an unsupported conference or workshop, you need to implement a 
subclass of ConferenceLike and the abstract method get_note_type. An example for such a subclass and method
is the class ICLR2019Conference. One sees that a forum consists
of multiple Note objects, which can be reviews, comments, etc.:

<div align="center">
  <img src="https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/forum_and_notes.png">
</div>

The purpose of get_note_type is
to return based on the content of a Note (see the 'content' key-value pair in above image)
the note type as a string. Between the following note types are distinguished in the following conferences and workshops:

##### Metareview, review, comment, paper

* ICLR.cc/2019/Conference/-/Blind_Submission

### Data Statistics

* ICLR
  * ICLR 2013
    * Metareview doesn't give a review score, but says for what the paper was accepted.
    * Normal reviews only consist of title and text + reviews and comments are not differentiated
    * PDFs aren't getting extracted. Presumably because pdf link doesn't point to pdf (it points to arxiv)
  * ICLR 2014
    * A lot of paper have as decision "decision": "submitted, no decision". Haven't checked if there are any with a different value
    * Normal reviews only consist of title and text
    * PDF: Same issues as ICLR 2013
  * ICLR 2017
    * Metareview doesn't give a review score, but says for what the paper was accepted. (differently than ICLR 2013 though). Maybe some give a review score in the comment
    * Normal reviews give confidence and rating
    * 3 Unknown types and 3 non-extracted PDFs
  * ICLR 2018
    * Metareview usually doesn't give a review score, but says for what the paper was accepted (like 2017). Some metareviews also have scores in the comment text though (see B1ae1lZRb).
    * Normal Review: Like ICLR 2017
    * 2 non-extracted PDFs
  * ICLR 2019
    * Metareview has a numerical confidence score and for what the paper was accepted (like 2017). 
    * Normal Review: Like ICLR 2017
  * ICLR 2020
    * Metareview: Like ICLR 2017
    * Normal Review: Gives rating score, but no confidence. Also has additional textual comments that haven't been seen before
  * ICLR 2021
    * Metareview isn't getting detected yet, as they get falsely recognized as comments
  * ICLR 2022
    * Metareview: Like ICLR 2017
    * Review: Main score is the "recommendation" score. Also has other scores about more fine-grained aspects of the reviewed submission
## TODOs

* Write Prof. Bruni overview of the different ICLR years
* Move ICLR comments to the classes and point it out in the README
* Write in README.md
  * Known problems and how to deal with them
    * Definitely run data_stats.py after extract_data.py  
    * ICLR 2019
      * SyMras0cFQ has withdrawal submission
  * Document about config.py
  * Document about ICLR 2019 and later
  * Update example of extracted datum
