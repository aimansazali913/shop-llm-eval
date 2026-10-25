import json, sys
import pandas as pd

r = json.load(open(sys.argv[1], encoding='utf-8'))
df = pd.read_csv('data/' + r['split'] + '.csv')
df['pred'] = r['preds']
bad = df[df['label'] != df['pred']]
bad.to_csv('docs/errors_' + r['split'] + '.csv', index=False)
print('saved', len(bad), 'errors')