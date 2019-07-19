from sklearn.feature_extraction.text import TfidfVectorizer

doc1 = "I like apples. I like oranges too"
doc2 = "I love apples. I hate doctors"
doc3 = "An apple a day keeps the doctor away"
doc4 = "Never compare an apple to an orange"

documents = [doc1, doc2, doc3, doc4]

tfidf = TfidfVectorizer().fit_transform(documents)
pairwise_sim = tfidf * tfidf.T

print pairwise_sim.A
# this is to compare the similarity 

# convert into 4 vectors
#1 means same 
#0 totally different.

#0.12 in the first row second column is the first file  compare with 2nd file 
# if it is over 0.8 then it is same but may express in differnet way