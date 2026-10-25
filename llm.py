import hashlib, json, os, sys, time
import pandas as pd
import requests
from config import LABELS, PROMPTS
from metrics import summarize 


URL = 'http://localhost:11434/api/generate'
CACHE = 'cache/llm_cache.jsonl'

def load_cache():
    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, encoding='utf-8') as f:
            for line in f:
                rec = json.loads(line)
                cache[rec['key']] = rec
    return cache

def make_key(model, prompt_name, text):
    return hashlib.sha256((model + '|' + prompt_name + '|' + text).encode('utf-8')).hexdigest()

def ask(model, prompt_name, text, cache):
    key = make_key(model, prompt_name, text)
    if key in cache:
        return cache[key]
    body = {'model': model, 'prompt': PROMPTS[prompt_name].format(text=text), 'stream': False,
            'options': {'temperature': 0, 'seed': 42, 'num_predict': 12}}
    start = time.time()
    reply = requests.post(URL, json=body, timeout=300)
    reply.raise_for_status()
    rec = {'key': key, 'raw': reply.json()['response'].strip().lower(), 'seconds': round(time.time() - start, 2)}
    cache[key] = rec
    os.makedirs('cache', exist_ok=True)
    with open(CACHE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + chr(10))
    return rec

def parse(raw):
    for label in LABELS:
        if label in raw:
            return label
    return 'invalid'

if __name__ == '__main__':
    model, prompt_name, split = sys.argv[1], sys.argv[2], sys.argv[3]
    df = pd.read_csv('data/' + split + '.csv')
    cache = load_cache()
    preds, secs = [], []
    for i, text in enumerate(df['text']):
        rec = ask(model, prompt_name, text, cache)
        preds.append(parse(rec['raw']))
        secs.append(rec['seconds'])
        if i % 20 == 0:
            print(i, 'of', len(df))
    out = summarize(df['label'].tolist(), preds)
    out.update({'model': model, 'prompt': prompt_name, 'split': split,
                'invalid_rate': preds.count('invalid') / len(preds),
                'mean_seconds': sum(secs) / len(secs), 'preds': preds})
    os.makedirs('results', exist_ok=True)
    name = model.replace(':', '-').replace('/', '-')
    with open('results/' + name + '_' + prompt_name + '_' + split + '.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print({k: v for k, v in out.items() if k != 'preds'})