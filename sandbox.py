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

infile = sys.argv[1] #get input argument: the training file
tri_counts= defaultdict(int)
bi_counts = defaultdict(int)
model = dict()
#MLE
def modelling(infile):
    infile = sys.argv[1]
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
    for trigram in tri_counts:
        model[trigram] = tri_counts[trigram] / bi_counts[trigram[:2]]
            
                
    