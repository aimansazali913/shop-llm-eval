import json, os, sys 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict
from sklearn.pipeline import make_pipeline
from metrics import summarize 

split = sys.argv[1]  # Get the split name from command line arguments
dev = pd.read_csv('data/dev.csv')  # Load the specified split
model = make_pipeline(TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5)), LogisticRegression(max_iter=1000))
if split == 'dev':
    truth = dev['label'].tolist()
    preds = list(cross_val_predict(model, dev['text'], dev['label'], cv=5))
else:
    other = pd.read_csv('data/' + split + '.csv')
    model.fit(dev['text'], dev['label'])
    truth = other['label'].tolist()
    preds = list(model.predict(other['text']))
out = summarize(truth, preds)
out.update({'model': 'tfidf-logreg', 'prompt': 'none', 'split': split, 'invalid_rate': 0.0, 'mean_seconds': 0.0, 'preds': preds})
os.makedirs('results', exist_ok=True)
with open('results/baseline_' + split + '.json', 'w') as f:
    json.dump(out, f, indent=2)
print({k: v for k, v in out.items() if k != 'preds'})