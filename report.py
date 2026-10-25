import glob, json

print('| model | prompt | split | n | accuracy | 95% CI | macro-F1 | invalid | sec/call |')
print('|---|---|---|---|---|---|---|---|---|')
for path in sorted(glob.glob('results/*.json')):
    r = json.load(open(path, encoding='utf-8'))
    print('| %s | %s | %s | %d | %.3f | %.3f-%.3f | %.3f | %.2f | %.2f |' % (
        r['model'], r['prompt'], r['split'], r['n'], r['accuracy'], r['ci_low'], r['ci_high'],
        r['macro_f1'], r['invalid_rate'], r['mean_seconds']))