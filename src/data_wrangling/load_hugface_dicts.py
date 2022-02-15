from datasets import load_dataset
from transformers import BertTokenizerFast

from OpenReviewLabRotation.src.config import PDF, REVIEW

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

# TODO: Change to longformer
tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
tokenizer.bos_token = tokenizer.cls_token
tokenizer.eos_token = tokenizer.sep_token

batch_size = 3  # change for full training
encoder_max_length = 512
decoder_max_length = 128


def process_data_to_model_inputs(batch):
    # tokenize the inputs and labels
    inputs = tokenizer(batch[PDF], padding="max_length", truncation=True, max_length=encoder_max_length, return_overflowing_tokens=True)
    inputs.data.pop('overflow_to_sample_mapping', None)
    outputs = tokenizer(batch[REVIEW], padding="max_length", truncation=True, max_length=decoder_max_length)
    outputs.data.pop('overflow_to_sample_mapping', None)

    # TODO: Put the inputs into a list. Required because of return_overflowing_tokens=True
    batch["input_ids"] = [inputs.input_ids]
    batch["attention_mask"] = [inputs.attention_mask]
    batch["decoder_input_ids"] = outputs.input_ids
    batch["decoder_attention_mask"] = outputs.attention_mask
    batch["labels"] = outputs.input_ids.copy()

    # because BERT automatically shifts the labels, the labels correspond exactly to `decoder_input_ids`.
    # We have to make sure that the PAD token is ignored
    batch["labels"] = [[-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]]

    return batch

if __name__ == "__main__":
    train_data = load_dataset("json", data_files="/home/work/PycharmProjects/BruniLabRotation/OpenReviewLabRotation/data/ICLR.cc/2022/Conference/-/Blind_Submission/hugface_dicts.json", field="data")
    train_data = train_data["train"]
    train_data = train_data.select(range(32))

    train_data = train_data.map(
        process_data_to_model_inputs,
        batched=True,
        batch_size=batch_size,
        remove_columns=[PDF, REVIEW]
    )
    train_data.set_format(
        type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
    )

### Some things I found online that might be useful. Has nothing to do with the rest of the code, just here for inspiration:

#  Like many question answering datasets, SQuAD-it uses the nested format, with all the text stored in a data field.
#  This means we can load the dataset by specifying the field argument as follows:
# data_files = {"train": "SQuAD_it-train.json", "test": "SQuAD_it-test.json"}
# squad_it_dataset = load_dataset("json", data_files=data_files, field="data")
# drug_dataset["train"].shuffle
# Dataset.filter() drop things
# return_overflowing_tokens=True in tokenization
"""

"""

"""
drug_dataset_clean = drug_dataset["train"].train_test_split(train_size=0.8, seed=42)
# Rename the default "test" split to "validation"
drug_dataset_clean["validation"] = drug_dataset_clean.pop("test")
# Add the "test" set to our `DatasetDict`
drug_dataset_clean["test"] = drug_dataset["test"]
drug_dataset_clean
"""