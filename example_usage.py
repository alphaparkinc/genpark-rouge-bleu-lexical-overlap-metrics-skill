from client import LexicalMetricsCalculator

ref = "Paxos ensures state machine replication consistency"
hyp = "Paxos guarantees consistency in state machine replication"

print("BLEU Score:", LexicalMetricsCalculator.calculate_bleu(ref, hyp))
print("ROUGE-L Score:", LexicalMetricsCalculator.calculate_rouge_l(ref, hyp))
