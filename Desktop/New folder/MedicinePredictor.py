###########################Note#####################
"""
    This module will predict the medicine based on the age,gender,symptoms

"""

"""
we are using dictionary for the input encoding purpose
Actually we are mapping symptom name to a particular number.
these numbers should be same as we have used earlier while
preprocessing the data.
preprocessing is done in superVisedLearning.py module.
"""



## I have made PKI file from dictionary object so that we can use it on server.

try:
    import cPickle as pickle
except:
    import pickle

## for regular expression.
import re


###################### Loading the objects which we have stored by using the superVisedLearning.py module. ################

symptomEncDecDictionary = pickle.load(open('symptomEncDecDictionary.pkl','rb'))
#print(symptomEncDecDictionary)

##similar to symptom's dictionary we have medicine dictionary
mediEncDecDictionary  = pickle.load(open('mediEncDecDictionary.pkl','rb'))
#print(mediEncDecDictionary)

## lastly the classifier
classifier = pickle.load(open('finalizedClassifier.pkl','rb'))


##################### Function to predict the medicine #####################################################################

def medicinePredictor(age,gender,symptoms):
    """
       This function takes input as:
       age = 20
       gender = "male" or "female"
       symptom = "weakness"

       e.g

       medicinePredictor(25,'male',['fever','weakness'])

       and returns the list of medicines.
    """
    try:
        age = int(age)
    except:
        return ["something wrong with the input"]

    if gender == 'male' or "Male" or "MALE":
        gender = 1
    elif gender == 'female' or "Female" or "FEMALE":
        gender = 0

#################### This can be used if the type of symptom is not a list of strings. Here type of symptom should be string only.        
##    symp     = symptomEncDecDictionary[symptom]
##    print(symp)
##
##    toPredict = [age,gender,symp]
##    print(toPredict)
##    encMedicine = classifier.predict([toPredict])
##    print(encMedicine)
##    medicine = mediEncDecDictionary[encMedicine[0]]
##    print(medicine)

    medicines = set()
    for symp in symptoms:
        #get the encoded symptom number
        symp     = symptomEncDecDictionary[symp]
        #print(symp)
        
        toPredict = [age,gender,symp]
        #print(toPredict)
        
        encMedicine = classifier.predict([toPredict])
        #print(encMedicine)

        #decoding the encMedicine number to string
        medicine = mediEncDecDictionary[encMedicine[0]]
        #print(medicine)

        #this will remove all the spaces from string of medicines
        medicine = re.sub(' +','',medicine)

        # this will extract everything in between the ' ' (quotes)
        medicine = re.findall(r"'([^']*)'",medicine)

        #updating the set of medicine .
        #Here all the repeated medicine will not be added again.
        #This is similar as taking union of medicines of all the symptoms.
        medicines.update(medicine)
        #print(medicines)

    # return the list of medicines    
    return (list(medicines))    
            
    
    






