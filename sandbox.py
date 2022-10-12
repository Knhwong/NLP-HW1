from importlib.metadata import distribution
import sys
from collections import defaultdict
import random

validCharacters = set("1234567890abcdefghijklmnopqrstuvwxyz. ")
def preprocess_line(line):
    valid = ""
    #.lower() automatically changes all capitals to lower.
    for i in line.lower():
        if i in validCharacters:
            if i in set("1234567890"):
                valid += "0"
            else:
                valid += i
        
    return valid



#Add Alpha ESTIMATION as the Easiest
#Need to deal with newLine and endLine
def modelling(infile, alpha):
    infile = sys.argv[1]
    tri_counts= defaultdict(int)
    bi_counts = defaultdict(int)
    model = dict()
    with open(infile) as f:
        for line in f:
            line = preprocess_line(line)
            
            for j in range(len(line)-3):
                trigram = line[j:j+3]
                tri_counts[trigram] += 1
                
                #Get Bigrams to Find Prob
                bigram = line[j:j+2]
                bi_counts[bigram] += 1
            
            f = len(line) - 3
            bigram = line[f:f+2]
            bi_counts[bigram] += 1

    #If we consider a|bc, bi_counts contains all trigram counts of bc occuring.
    #Switch to add alpha of 0.05
    for state in bi_counts:
        #build probability distribution
        distribution = []
        letter = []
        for c in validCharacters:
            #state+c is the trigram
            prob = (tri_counts.get(str(state+c),0) + alpha) / (bi_counts[state] + (len(validCharacters)*alpha))
            distribution.append(prob)
            letter.append(c)
        #We seperate the two rather than using a tuple so we can easily weigh later on.
        model[state] = (letter, distribution)

    return model

def generate_from_LM(model):
    fullState = ["#","#"]
    for j in range(1,300):
        state = fullState[j] + fullState[j-1]
        nextState = random.choices(model[state][0], model[state][1])
        fullState.append(nextState)
    print(str(fullState))
 
def printModel(model):
    for state in sorted(model.keys()):
        for i in range(len(validCharacters)):
            print(state + model[state][0][i] + "|" + str(model[state][1][i]))
        
        #print("(" + str(trigram[2]) + "|" + str(trigram[:2]) + "):" + str(model[trigram]))

#0-2 Trigram
#4-13 Probability
def importModel(infile):
    model = dict()
    s = 0
    with open(infile) as f:
        for line in f:
            model[line[:3]] = float(line[4:14])
    return model

    
infile = sys.argv[1] #get input argument: the training file
#infile2 = sys.argv[2]

#modelBR = importModel(infile2)
model = modelling(infile, 0.1)
generate_from_LM(model)
#printModel(model)
            
                
    