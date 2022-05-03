import os
import argparse
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
import jsonlines
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

class News_Dataset(Dataset):
    def __init__(self, file):
        self.article = []
        self.id = []
        with jsonlines.open(file) as f:
            for obj in f:
                self.article.append(obj["maintext"])
                self.id.append(obj["id"])
    
    def __len__(self):
        return len(self.id)

    def __getitem__(self, idx):
        return self.article[idx], self.id[idx]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--article", 
        type=Path,
        help="Path to the article jsonl file.",
        required=True
        )
    parser.add_argument(
        "-s", "--summary", 
        type=Path,
        help="Path to the summary jsonl file.",
        required=True
        )
    parser.add_argument(
        "-m", "--model", 
        type=Path,
        help="Path to the model folder.",
        required=True
        )
    parser.add_argument(
        "--max_length", 
        type=int,
        help="Max output length.",
        default=128
        )
    
    parser.add_argument(
        "--greedy", 
        help="Greedy search.",
        action="store_true"
        )
    parser.add_argument(
        "--beam", 
        type=int,
        help="Beam search."
        )
    parser.add_argument(
        "--top_k", 
        type=int,
        help="Top-k Sampling."
        )
    parser.add_argument(
        "--top_p", 
        type=float,
        help="Top-p Sampling."
        )
    parser.add_argument(
        "--temperature", 
        type=float,
        help="Temperature."
        )

    args = parser.parse_args()
    assert os.path.splitext(args.article)[-1] == ".jsonl" and os.path.splitext(args.summary)[-1] == ".jsonl"

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    test_set = News_Dataset(args.article)
    test_loader = DataLoader(test_set, num_workers=8)

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model).to(device)
    
    sample = not args.greedy and args.beam is None

    with jsonlines.open(args.summary, "w") as writer:
        for article, id in tqdm(test_loader):
            input_ids = tokenizer.encode(article[0], return_tensors='pt').to(device)
            
            output = model.generate(input_ids, max_length=args.max_length, do_sample=sample, num_beams=args.beam, temperature=args.temperature, top_k=args.top_k, top_p=args.top_p)
            writer.write({
                "title": tokenizer.decode(output[0], skip_special_tokens=True),
                "id": id[0]
            })
