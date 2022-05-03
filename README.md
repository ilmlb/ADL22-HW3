# ADL22-HW3
Dataset & evaluation script for ADL 2022 homework 3

## Dataset
[download link](https://drive.google.com/file/d/186ejZVADY16RBfVjzcMcz9bal9L3inXC/view?usp=sharing)

## Installation
```
git clone https://github.com/ilmlb/ADL22-HW3.git
cd ADL22-HW3
pip install -e tw_rouge
```


## Usage
### Training
The training script is simply modified from [huggingface summarization](https://github.com/huggingface/transformers/blob/main/examples/pytorch/summarization/run_summarization.py). Therefore, we have to convert our input `.jsonl` files to the required `.csv` format. 
```
python jsonl_to_csv.py <-i json_file> <-o csv_file>
[CUDA_VISIBLE_DEVICES=0,1,...] python run_summarization.py <--model_name_or_path model> [<--do_train> <--train_file csv_file>] [<--do_eval> <--validation_file public_csv>] [--text_column text] [--summary_column summary] <--output_dir dir> [--warmup_ratio ratio] [--num_train_epochs epoch]
```
- `-i`, `--input_jsonl`: Path to the jsonl file input.
- `-o`, `--output_csv`: Path to the csv file output.
- `CUDA_VISIBLE_DEVICES=0`: Training with GPU.
- `--model_name_or_path`: Path to pretrained model or model identifier from huggingface.co/models (default: None)
- `--do_train`: Whether to run training. (default: False)
- `--train_file`: The input training data file (a json or csv file). (default: None)
- `--do_eval`: Whether to run eval on the dev set. (default: False)
- `--validation_file`: The input validation data file (a json or csv file). (default: None)
- `--text_column`: The name of the column in the datasets containing the full texts (for summarization). (default: None)
- `--summary_column`: The name of the column in the datasets containing the summaries (for summarization). (default: None)
- `--output_dir`: The output directory where the model predictions and checkpoints will be written. (default: None)
- `--warmup_ratio`: Linear warmup over warmup_ratio fraction of total steps. (default: 0.0)
- `--num_train_epochs`: Total number of training epochs to perform. (default: 3.0)

### Inference
```
python predict.py <-a test_file> <-s result_file> <-m model> [--max_length length] [--greedy] [--beam num] [--top_k k] [--top_p p] [--temperature t]
```
- `-a`, `--article`: Path to the article jsonl file. 
- `-s`, `--summary`: Path to the summary jsonl file.
- `-m`, `--model`: Path to the model folder.
- `--max_length`: Max output length. (default: 128)
- `--greedy`: Greedy search. (default: None)
- `--beam`: Beam search. (default: None)
- `--top_k`: Top-k Sampling. (default: None)
- `--top_p`: Top-p Sampling. (default: None)
- `--temperature`: Temperature. (default: None)

### Evaluation
#### Use the Script
```
usage: eval.py [-h] [-r REFERENCE] [-s SUBMISSION]

optional arguments:
  -h, --help            show this help message and exit
  -r REFERENCE, --reference REFERENCE
  -s SUBMISSION, --submission SUBMISSION
```

Example:
```
python eval.py -r public.jsonl -s submission.jsonl
{
  "rouge-1": {
    "f": 0.21999419163162043,
    "p": 0.2446195813913345,
    "r": 0.2137398792982201
  },
  "rouge-2": {
    "f": 0.0847583291303246,
    "p": 0.09419044877345074,
    "r": 0.08287844474014894
  },
  "rouge-l": {
    "f": 0.21017939117006337,
    "p": 0.25157090570020846,
    "r": 0.19404349000921203
  }
}
```


#### Use Python Library
```
>>> from tw_rouge import get_rouge
>>> get_rouge('我是人', '我是一個人')
{'rouge-1': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}, 'rouge-2': {'f': 0.33333332888888895, 'p': 0.5, 'r': 0.25}, 'rouge-l': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}}
>>> get_rouge(['我是人'], [ 我是一個人'])
{'rouge-1': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}, 'rouge-2': {'f': 0.33333332888888895, 'p': 0.5, 'r': 0.25}, 'rouge-l': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}}
>>> get_rouge(['我是人'], ['我是一個人'], avg=False)
[{'rouge-1': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}, 'rouge-2': {'f': 0.33333332888888895, 'p': 0.5, 'r': 0.25}, 'rouge-l': {'f': 0.7499999953125, 'p': 1.0, 'r': 0.6}}]
```


## Reference
[cccntu/tw_rouge](https://github.com/cccntu/tw_rouge)
