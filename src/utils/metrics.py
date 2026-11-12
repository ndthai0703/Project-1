import re
import unicodedata
from collections import Counter

def normalize(s):
    s=unicodedata.normalize("NFC",s).casefold()
    return " ".join(re.sub(r"[^\w\s]"," ",s).split())
def f1(a,b):
    a,b=normalize(a).split(),normalize(b).split()
    if not a or not b: return float(a==b)
    return 2*sum((Counter(a)&Counter(b)).values())/(len(a)+len(b))
def score(pred,refs):
    return {"exact_match":max(float(normalize(pred)==normalize(r)) for r in refs),
            "token_f1":max(f1(pred,r) for r in refs)}
