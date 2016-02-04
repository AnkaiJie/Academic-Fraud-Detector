'''
Created on Feb 1, 2016

@author: Ankai
'''

import re
from WordInference import inferSpaces


# splits whole reference string into individual reference strings
def bulkSplit(section):
    bracket_form = re.compile(r'\[.*?\]')    
    out = [x for x in bracket_form.split(section) if x]
    
    return out

# splits citation into its components and returns a citation object
def citeSplit(citation):
    firstSplit = citation.replace("and", " LAST_AUTHOR: ", 1).replace(',', ' ').replace('.', ' ')
    firstSplit = firstSplit.split()
    #print(firstSplit)
    
    
    # variables to keep track of where we are in the loop
    finishedAuthors = 0
    finishedTitle = 0
    lastAuthor = 0
    
    # tempVariables to be modified
    tempInitial = ""
    authorArray = []
    year = 0
    title = ""
    
    for idx, el in enumerate(firstSplit):
        #parses the author section
        if (finishedAuthors is 0):
            if (el == "LAST_AUTHOR:"):
                lastAuthor = 1
                continue
            elif (len(el) is 1):
                tempInitial += el + '.'  
            elif (tempInitial==""):
                finishedAuthors = 1
            elif (tempInitial != ""):
                tempInitial += ' '
                author = tempInitial + el
                tempInitial = ""
                authorArray.append(author)
                if (lastAuthor is 1):
                    finishedAuthors = 1
        #gets the year and the title, assuming they come after the author
        if (finishedTitle is 0 and finishedAuthors is 1):
            possibleYr = el.replace('(', '').replace(')', '')
            if (el=='LAST_AUTHOR:'):
                continue
            if (possibleYr.isdigit()):
                #print('in if ' + el)
                year = int(possibleYr)
                
            else:
                #print('in else ' + el)
                title += inferSpaces(el) + ' '
                if (firstSplit[idx+1]!= 'LAST_AUTHOR:'):
                    finishedTitle = 1
    
    # if year was not before the title, it is usually put at the end
    if (year == 0):
        year = firstSplit[-1]
        
    infoDict = {'authors': authorArray, 'title': title.strip(), 'year': year}
    return infoDict    
    
    


#print (citeSplit("r.j.adamsandb.hannaford.(2009).stablehapticinteractionwithvirtualenvironments.ieeetransactionsonroboticsandautomation,15(3):465-474,1999."))


'''r.j.adamsandb.hannaford.stablehapticinteractionwithvirtualenvironments.ieeetransactionsonroboticsandautomation,15(3):465-474,1999.'''
