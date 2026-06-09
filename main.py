from classes.hybrid_retriever import HybridRetriever

retriever = HybridRetriever()

for i in retriever.retrieve("What is a Turing Machine?"):
    print(i)