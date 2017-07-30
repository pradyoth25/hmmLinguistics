import nltk
path = nltk.data.path[0] + '/corpora/brown/brown_100.txt'
readPath = nltk.data.path[0] + '/corpora/brown/brown_vocab_100.txt'
import numpy as np

counts = np.zeros(813)

wordDict = {}

with open(readPath, 'r') as inputFile:
	for count, line in enumerate(inputFile):
		wordDict[line.rstrip()] = count
		

with open(path, 'r') as inputFile:
	for line in inputFile:
		line = line.rstrip('\n')
		words = line.split(' ')
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('</s>')
		# print words
		for word in words:
			# print word
			if word in wordDict.keys():
				counts[wordDict[word]] += 1



# print counts
probs = counts/np.sum(counts)
# print probs
with open('unigram_probs.txt', 'w') as probFile:
	probFile.write(str(probs))

# cnt = 0
# for element in counts:
# 	if element == 1:
# 		cnt +=1

# print cnt/813.0
sentenceListProb = []
perplexityList = []
toyPath = nltk.data.path[0] + '/corpora/brown/toy_corpus.txt'
with open(toyPath, 'r') as corpusFile2:
	for line in corpusFile2:
		line = line.rstrip('\n')
		words = line.split(' ')
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('</s>')
		sentprob = 1
		wordCount = 0
		for word in words: 
			wordprob = probs[wordDict[word]]
				# print word
				# print "wordProb is", wordprob
			sentprob *= wordprob
				# print "sentenceProb so far is", sentprob
			wordCount +=1
		sentenceListProb.append(sentprob)
			# print wordCount
		perplexity = 1/(pow(sentprob, 1.0/wordCount))
		perplexityList.append(perplexity)
		
# print sentenceListProb
# print perplexityList

with open('unigram_eval.txt', 'a') as finalFile:
	# for prob in sentenceListProb:
	# 	finalFile.write(str(prob)+"\n")
	for perplex in perplexityList:
		finalFile.write(str(perplex)+"\n")