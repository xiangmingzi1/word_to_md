from transformers import BertTokenizer

# 初始化 tokenizer
TOKENIZER = BertTokenizer.from_pretrained("bert-base-chinese")

# 配置参数
SEGMENT_SEPARATOR = "&&&&&"
NAMESPACES = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}