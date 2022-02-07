# OpenReviewLabRotation

## Examples

* [Example of extracted data](https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/SkgkJn05YX.json)

## How-TOs

### Extracting Data

All the data extraction logic is contained in extract_data.py.
To extract data, run extract_data.py as __main__. Make sure to take a look at what arguments the ArgumentParser takes.
After extracting data, make sure to run data statistics and check them.

#### OpenReview Python Client

Definitely check out the [OpenReview Python Client](https://openreview-py.readthedocs.io/en/latest/), as it gets used. 
The documentation is short and easy to read, so no worries. 

Especially https://openreview-py.readthedocs.io/en/latest/get_submission_invitations.html#getting-submissions
 is interesting for finding ids of conferences, workshops, etc. to extract data from them.



#### Extracting data from an unsupported conference or workshop

To see from what invitation ids the extracting data is supported, see "invitation_id" of the classes in "extract_data.py".

To extract data from an unsupported conference or workshop, you need to implement a 
subclass of ConferenceLike and its abstract method get_note_type. One sees that a forum consists
of multiple Note objects, which can be reviews, comments, etc.:

<div align="center">
  <img src="https://github.com/HSinger04/OpenReviewLabRotation/blob/main/assets/forum_and_notes.png">
</div>

The purpose of get_note_type is
to return based on the content of a Note (see the 'content' key-value pair in above image)
the note type as a string. To see a list of available or add new note types, please use config.py

### Information of specific conferences and workshops

To see for what conferences and workshops have already been implemented, see the subclasses
of ConferenceLike in "extract_data.py". Make sure to especially read their doc string.
There, under TODO, bugs are also documented.


## TODOs