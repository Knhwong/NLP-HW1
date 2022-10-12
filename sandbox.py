from importlib.metadata import distribution
import sys
from collections import defaultdict

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
        model[state] = (letter, distribution)
        print(sum(distribution));
    
    
    #for trigram in tri_counts:
        #model[trigram] = tri_counts[trigram] / bi_counts[trigram[:2]]
    return model
 
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
#printModel(model)
            
                
    