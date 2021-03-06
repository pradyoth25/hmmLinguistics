import numpy as np

opFile = open('problem4.txt', 'w')
words = ["young","man","wall"]
wordDict = { "young" : 0, "man" : 1, "wall": 2}
transitionMatrix = np.array(([0.3, 0, 0.5], [0.8, 0.2, 0], [0.6, 0.2, 0]))
emissionMatrix = np.array(([0.2, 0.4, 0.4], [1, 0, 0], [0, 0.5, 0.5]))
startProb = np.array([0.8, 0.2, 0])
endProb = np.array([0.2, 0, 0.2])

viterbiMatrix = np.zeros((len(transitionMatrix), len(words)))
wordIndex = wordDict[words[0]]
nodeCount = 1

for i in range(len(transitionMatrix)):
    viterbiMatrix[i][0] = startProb[i]*emissionMatrix[i][wordIndex]
    print viterbiMatrix[i][0], "for node", nodeCount
    opFile.write(str(str(viterbiMatrix[i][0]) + "for node" + str(nodeCount)) + "\n")
    nodeCount +=1
    print "----------------"
    opFile.write("----------------"+ "\n")
# print viterbiMatrix

for i in range(1, len(words)):
    wordIndex = wordDict[words[i]]
    for j in range(len(transitionMatrix)):
        wordProbs = [viterbiMatrix[k][i-1] * transitionMatrix[k][j] for k in range(len(transitionMatrix))]
        probSum = max(wordProbs)
        viterbiMatrix[j][i] = emissionMatrix[j][wordIndex] * probSum
        print "the values for this node can be taking the max of", wordProbs, "and multiplying it by", emissionMatrix[j][wordIndex]
        print "this is equal to", probSum, "*", emissionMatrix[j][wordIndex], "=", viterbiMatrix[j][i]
        print viterbiMatrix[j][i], "is the final value for the node", nodeCount
        print "---------------------"
        opFile.write(str("the values for this node can be calculated by taking the maximum of" + str(wordProbs) + "and multiplying it by" + str(emissionMatrix[j][wordIndex])) + "\n")
        opFile.write(str("this is equal to" + str(probSum) + "*" + str(emissionMatrix[j][wordIndex]) + "=" + str(viterbiMatrix[j][i])) + "\n")
        opFile.write(str(str(viterbiMatrix[j][i]) + "is the final value for the node" + str(nodeCount)) + "\n")
        opFile.write("---------------------" + "\n")
        nodeCount+=1

print "the viterbi matrix is"
print viterbiMatrix

opFile.write("the viterbi matrix is"+ "\n")
opFile.write(str(viterbiMatrix) + "\n")

finalProbs = [endProb[i] * viterbiMatrix[i][len(words)-1] for i in range(len(transitionMatrix))]
# print finalProbs
pathCount = 1
print "in order to find the final probability"
opFile.write("in order to find the final probability" + "\n")
for p in finalProbs:
    print "the probability of path", pathCount, "is", p
    opFile.write(str("the probability of path" + str(pathCount) + "is" + str(p)) + "\n")
    pathCount += 1
    print "--------------------------"
    opFile.write("--------------------------"+ "\n")

print "the final probability is the maximum of all three paths"
opFile.write("the final probability is the maxmimum of all three paths" + "\n")
result = max(finalProbs)
print result
opFile.write(str(result)+ "\n")

opFile.close()