from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

MAX_TOKENS = 2000
SEGMENT_SEPARATOR = "*****"
