from importlib.metadata import distribution
import sys
from collections import defaultdict
import random

validCharacters = set("1234567890abcdefghijklmnopqrstuvwxyz. ")
vocabulary = " #.0abcdefghijklmnopqrstuvwxyz"
def preprocess_line(line):
    valid = "##"
    #.lower() automatically changes all capitals to lower.
    for i in line.lower():
        if i in validCharacters:
            if i in set("1234567890"):
                valid += "0"
            else:
                valid += i
    valid += "#"
    return valid



#Add Alpha ESTIMATION as the Easiest
#Need to deal with newLine and endLine
def modelling(infile, alpha):
    tri_counts= defaultdict(int)
    bi_counts = defaultdict(int)
    model = dict()
    with open(infile) as f:
        for line in f:
            line_ = preprocess_line(line)
            
            for j in range(len(line_)-2):
                trigram = line_[j:j+3]
                tri_counts[trigram] += 1
                
                #Get Bigrams to Find Prob
                bigram = line_[j:j+2]
                bi_counts[bigram] += 1
            
            f = len(line_) - 3
            bigram = line_[f:f+2]
            bi_counts[bigram] += 1
            
    n = len(vocabulary)
    for uni in vocabulary:
        for bi in vocabulary:
            state = uni + bi
            distribution = []
            letters = []
            for tri in vocabulary:
                prob = (tri_counts.get(str(state+tri),0) + alpha) / (bi_counts[state] + (n*alpha))
                distribution.append(prob)
                letters.append(tri)
            model[state] = (letters, distribution)
        
    return model

def generate_from_LM(model):
    fullState = "##"
    for j in range(1,300):
        state = fullState[j-1] + fullState[j]
        nextState = random.choices(model[state][0], model[state][1])
        fullState += (nextState[0])
    fullState = fullState[3:].replace("#", "\n")
    return fullState
 
def printModel(model):
    for state in sorted(model.keys()):
        for i in range(len(model[state][0])):
            print(state + model[state][0][i] + "|" + str(model[state][1][i]))
        

#0-2 Trigram
#4-13 Probability
def importModel(infile):
    model = dict()
    with open(infile) as f:
        for line in f:
            #[:2] = State
            state = line[:2]
            letter = line[2]
            prob = float(line[4:14])
            
            if state in model:
                model[state][0].append(letter)
                model[state][1].append(prob)
            else:
                distribution = [prob]
                letters = [letter]
                model[state] = (letters, distribution)
                
    return model

    
model = modelling('training.en', 0)
modelBR = importModel('model-br.en')
#printModel(model)
randomString = generate_from_LM(model)
print(randomString)
            
                
    