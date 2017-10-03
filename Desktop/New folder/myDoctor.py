from flask import Flask,render_template, url_for, request,redirect,Response,jsonify
from flask_ask import Ask, statement, question,session
import json,random,string
import requests,time,unidecode


app = Flask(__name__)
ask = Ask(app,"/myDoctor")

secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits)
                     for x in xrange(32))
app.secret_key = secret_key
        

###### File Name ############# Function Name ####
from MedicinePredictor import medicinePredictor 


@ask.launch
def start_skill():
	welcome_message = 'Hello , I am your personal Doctor. I can analyze your symptoms and suggest you some medicines. Tell me your gender and age ?'
	print("launchIntent")
	return question(welcome_message)

@ask.intent('infoIntent',convert = {'gender':str,'age':int})
def sayInfo(gender,age):
        print("infoIntent")
        #session.clear()
        print(age)
        session.attributes['gender'] = gender
        session.attributes['age']  = age
        print(gender,age)
        print(session.attributes['gender'],session.attributes['age'])
        try:
                symptoms = session.attributes['symptoms']
                if type(symptoms)!= list :
                        symptoms = symptoms.split(' ')    #this is to make a list of symptoms
                symptoms = [str(x) for x in symptoms ]
                print("inside sayInfo",symptoms)
                msg = "you have following symptoms {} Do you want me to analyze them to suggest you medicines?".format(' '.join(symptoms))
                return question(msg)
        except (KeyError):
                msg = "Hello, tell me your symptoms? "
                return question(msg)

@ask.intent("readSymptoms",convert = {'symptoms':str})
def symptomReader(symptoms):
        print("readSymptomsIntent")
        symptoms = symptoms.split(' ')    #this is to make a list of symptoms
        symptoms = [str(x) for x in symptoms ]
        print("inside symptomreader",symptoms)
        try:
                session.attributes['symptoms'] = symptoms
                age = session.attributes['age']
        except (KeyError):
                return question("Please tell me What's your gender and age?")
        
        #print(symptoms)
        msg = "you have following symptoms {} Do you want me to analyze them to suggest you medicines?".format(' '.join(symptoms))
        return question(msg)

@ask.intent("yesIntent")
def yes():
        print("yesIntent")
        try:
                age = session.attributes['age']
                symptoms = session.attributes['symptoms']
                gender  = session.attributes['gender']
        except (KeyError):
                return question("Please tell me the symptoms ?")
        #print(symptoms)
        if type(symptoms)!= list :
                symptoms = symptoms.split(' ')    #this is to make a list of symptoms
        symptoms = [str(x) for x in symptoms ]
        print("inside yesIntent",symptoms)
        session.clear()
        msg = predictMedicine(age,symptoms,gender)
        return statement(msg)
                
       

def predictMedicine(age,symptoms,gender = 'male'):
        print(age,symptoms,gender)
        apiDoc = """
        This function takes input as:
               age = 20
               gender = "male" or "female"
               symptom = "weakness"
               e.g
               medicinePredictor(25,'male',['fever','weakness'])
               and returns the list of medicines.
            """

        if (isinstance(age,int)) & (isinstance(gender,str)  | isinstance(gender,unicode)) & (isinstance(symptoms,list)) is not True:
            return "something went wrong."
        
        predictedMedicines = medicinePredictor(age,gender,symptoms)
        msg = ' '.join(predictedMedicines) 
        return msg
    


if __name__ == '__main__':
	app.run(debug=False)

