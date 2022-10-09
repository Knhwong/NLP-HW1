#Just for testing
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

print(preprocess_line("12371381289312ASHDJHDJSHDJHDJA;';s';xzczczxccxzfsd..ad,asd  asdasd**&##"))