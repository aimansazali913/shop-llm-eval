import json
import pandas as pd
from config import LABELS
from llm import parse

def test_labels_valid():
    for f in ['data/dev.csv', 'data/test.csv', 'data/adversarial.csv']:
        assert set(pd.read_csv(f)['label']) <= set(LABELS)

def test_no_overlap():
    dev = set(pd.read_csv('data/dev.csv')['text'])
    test = set(pd.read_csv('data/test.csv')['text'])
    assert not dev & test

def test_parse():
    assert parse('payment_issue') == 'payment_issue'
    assert parse('hello') == 'invalid'

def test_baseline_floor():
    r = json.load(open('results/baseline_dev.json'))
    assert r['macro_f1'] >= 0.60