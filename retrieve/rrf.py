from collections import defaultdict

def rrf(rank_lists, k=60):
    scores = defaultdict(float)

    for ranked_list in rank_lists:
        for rank, doc_id in enumerate(ranked_list, start=1):
            scores[int(doc_id)] += 1 / (k + rank)

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )