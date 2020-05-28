import os
import random
import logging

import torch
import numpy as np

from sklearn.metrics import precision_recall_fscore_support, accuracy_score

from model import ElectraForMultiLabelClassification

from transformers import (
    ElectraConfig,
    ElectraTokenizer,
)

from tokenization_kocharelectra import KoCharElectraTokenizer

CONFIG_CLASSES = {
    "koelectra-small": ElectraConfig,
    "koelectra-base": ElectraConfig,
    "kocharelectra-base": ElectraConfig,
    "kocharelectra-small": ElectraConfig
}

TOKENIZER_CLASSES = {
    "koelectra-small": ElectraTokenizer,
    "koelectra-base": ElectraTokenizer,
    "kocharelectra-base": KoCharElectraTokenizer,
    "kocharelectra-small": KoCharElectraTokenizer
}

MODEL_CLASSES = {
    "koelectra-small": ElectraForMultiLabelClassification,
    "koelectra-base": ElectraForMultiLabelClassification,
    "kocharelectra-base": ElectraForMultiLabelClassification,
    "kocharelectra-small": ElectraForMultiLabelClassification
}


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


def compute_metrics(labels, preds):
    assert len(preds) == len(labels)
    results = dict()

    results["accuracy"] = accuracy_score(labels, preds)
    results["macro_precision"], results["macro_recall"], results[
        "macro_f1"], _ = precision_recall_fscore_support(
        labels, preds, average="macro")
    results["micro_precision"], results["micro_recall"], results[
        "micro_f1"], _ = precision_recall_fscore_support(
        labels, preds, average="micro")
    results["weighted_precision"], results["weighted_recall"], results[
        "weighted_f1"], _ = precision_recall_fscore_support(
        labels, preds, average="weighted")

    return results
