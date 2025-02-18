import torch
from tqdm import tqdm
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import load_from_disk
from rouge_score import rouge_scorer
from src.TextSummarizer.entity import ModelEvaluationConfig
class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        """Split the dataset into smaller batches that we can process simultaneously."""
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i: i + batch_size]

    def calculate_metric_on_test_ds(self, dataset, scorer, model, tokenizer,
                                    batch_size=16, device="cuda" if torch.cuda.is_available() else "cpu",
                                    column_text="article", column_summary="highlights"):
        # Split the dataset into batches
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        # Initialize score dictionary for the ROUGE metrics
        scores = {metric: [] for metric in ["rouge1", "rouge2", "rougeL", "rougeLsum"]}

        # Iterate through batches to generate summaries
        for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total=len(article_batches)):
            # Tokenize input articles
            inputs = tokenizer(article_batch, max_length=1024, truncation=True,
                               padding="max_length", return_tensors="pt")
            
            # Generate summaries using the model
            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                                       attention_mask=inputs["attention_mask"].to(device),
                                       length_penalty=0.8, num_beams=8, max_length=128)

            # Decode the generated summaries
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                                  clean_up_tokenization_spaces=True) for s in summaries]

            decoded_summaries = [d.replace("", " ") for d in decoded_summaries]

            # Compute ROUGE scores for each prediction-reference pair
            for prediction, reference in zip(decoded_summaries, target_batch):
                score = scorer.score(reference, prediction)
                for metric in scores.keys():
                    scores[metric].append(score[metric].fmeasure)

        # Calculate the average scores for each metric
        avg_scores = {metric: sum(scores[metric]) / len(scores[metric]) for metric in scores}
        return avg_scores

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
       
        # Load data
        dataset_samsum_pt = load_from_disk(self.config.data_path)

        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        # Initialize RougeScorer from rouge-score
        scorer = rouge_scorer.RougeScorer(rouge_names)

        # Calculate metrics on the test dataset
        score = self.calculate_metric_on_test_ds(
            dataset_samsum_pt['test'][0:10], scorer, model_pegasus, tokenizer, batch_size=2,
            column_text='dialogue', column_summary='summary'
        )

        # Store the ROUGE scores in a dictionary
        rouge_dict = {rn: score[rn] for rn in rouge_names}

        # Save the ROUGE scores to a CSV file
        df = pd.DataFrame(rouge_dict, index=['pegasus'])
        df.to_csv(self.config.metric_file_name, index=False)
