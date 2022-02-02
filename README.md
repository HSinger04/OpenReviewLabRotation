# OpenReviewLabRotation

## Examples

* [Example of extracted data](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/SkgkJn05YX.json)

## How-TOs

### Extracting Data

All the data extraction logic is contained in extract_data.py.
To extract data, run extract_data.py as __main__. Make sure to take a look at what arguments the ArgumentParser takes.

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
the note type as a string (e.g. review, comment, etc.). 


## TODOs

* requirements.txt
* Pointer and doc on OpenReview's API
* Convert binary pdf to text

### Question for Prof. Bruni

* What should we do with comments / reply chains?
* What should I do with information outside of content?

