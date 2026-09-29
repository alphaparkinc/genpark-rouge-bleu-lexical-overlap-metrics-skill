"""Pure Python ROUGE & BLEU Lexical Metrics.
100% Python Standard Library.
"""

import math
import collections
import re

class LexicalMetricsCalculator:
    """Calculates BLEU and ROUGE-L lexical overlap scores without external libraries."""
    @staticmethod
    def get_ngrams(tokens, n):
        return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

    @classmethod
    def calculate_bleu(cls, reference, hypothesis, max_n=2):
        ref_tokens = re.findall(r'\b\w+\b', reference.lower())
        hyp_tokens = re.findall(r'\b\w+\b', hypothesis.lower())
        if not hyp_tokens:
            return 0.0
        precisions = []
        for n in range(1, max_n + 1):
            ref_ngrams = collections.Counter(cls.get_ngrams(ref_tokens, n))
            hyp_ngrams = collections.Counter(cls.get_ngrams(hyp_tokens, n))
            clipped = sum(min(count, ref_ngrams.get(ng, 0)) for ng, count in hyp_ngrams.items())
            total = sum(hyp_ngrams.values()) or 1
            precisions.append(clipped / total)
        bp = 1.0 if len(hyp_tokens) > len(ref_tokens) else math.exp(1 - len(ref_tokens) / max(len(hyp_tokens), 1))
        geo_mean = math.exp(sum(math.log(max(p, 1e-6)) for p in precisions) / len(precisions))
        return round(bp * geo_mean, 4)

    @classmethod
    def calculate_rouge_l(cls, reference, hypothesis):
        ref_tokens = re.findall(r'\b\w+\b', reference.lower())
        hyp_tokens = re.findall(r'\b\w+\b', hypothesis.lower())
        m, n = len(ref_tokens), len(hyp_tokens)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if ref_tokens[i] == hyp_tokens[j]:
                    dp[i+1][j+1] = dp[i][j] + 1
                else:
                    dp[i+1][j+1] = max(dp[i+1][j], dp[i][j+1])
        lcs = dp[m][n]
        p = lcs / max(n, 1)
        r = lcs / max(m, 1)
        f1 = (2 * p * r) / max(p + r, 1e-6)
        return {"precision": round(p, 4), "recall": round(r, 4), "f1": round(f1, 4)}
