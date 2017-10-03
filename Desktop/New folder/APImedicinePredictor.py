from flask import Flask,render_template, url_for, request,redirect,Response,jsonify


###### File Name ############# Function Name ####
from MedicinePredictor import medicinePredictor 

app = Flask(__name__)


@app.route('/mPredictor',methods=['POST','GET'])
def predictMedicine():
    apiDoc = """
       This function takes input as:
       age = 20
       gender = "male" or "female"
       symptom = "weakness"

       e.g


       medicinePredictor(25,'male',['fever','weakness'])

       and returns the list of medicines.
    """
    
    if request.method == "POST" and request.headers['content-type'] == 'application/json':
        requestedData = request.get_json()
        age              = requestedData['age']
        gender           = requestedData['gender']
        symptoms         = requestedData['symptoms']

        if (isinstance(age,int)) & (isinstance(gender,str)  | isinstance(gender,unicode)) & (isinstance(symptoms,list)) is not True:
            return jsonfiy(msg= apiDoc)
        
        predictedMedicines = medicinePredictor(age,gender,symptoms)
        medicine = {"medicines":predictedMedicines} 
        return jsonify(msg = medicine)
    




if __name__ == "__main__":
    app.run(port = 5050,debug=False)
