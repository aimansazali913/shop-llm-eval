import math 
from sklearn.metrics import f1_score
from config import LABELS 

def wilson(correct, n, z=1.96):
    p = correct / n
    denom = 1 + z*z / n
    centre = (p + z*z / (2*n)) / denom
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return centre - half, centre + half

def summarize(truth, pred):
    correct = sum(t == p for t, p in zip(truth, pred))
    n = len(truth)
    correct = sum(t == p for t, p in zip(truth, pred))
    low, high = wilson(correct, n) 
    macro=f1 = f1_score(truth, pred, average='macro', labels=LABELS, zero_division=0)
    return {'n': n, 'correct': correct, 'accuracy': correct/n, 'accuracy_ci': (low, high), 'macro_f1': macro
    }
