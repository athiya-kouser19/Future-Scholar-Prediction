
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import os
from sklearn.linear_model import LinearRegression



app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict', methods=['POST', 'GET'])  # route to show the predictions in a web UI
@cross_origin()
def index():
    

    if request.method == 'POST':
        try:
            # Reading the inputs given by the user
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            research = 1 if is_research.lower() == 'yes' else 0
            
            # Define the path to the model file
            filename = 'D:\phase1\future\Admission-Prediction-main\Admission_Prediction\finalized_model.pickle.url'
            
            # Check if the model file exists
            if not os.path.exists(filename):
                return 'Model file not found.'
            
            # Load the model from the file
            with open(filename, 'rb') as file:
                loaded_model = pickle.load(file)
            
            # Predictions using the loaded model
            prediction = loaded_model.predict([[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]])
            print('prediction is', prediction)
            
            # Showing the prediction results in a UI
            return render_template('results.html', prediction=round(100 * prediction[0]))
        
        except Exception as e:
            print('The Exception message is: ', e)
            return 'Something went wrong: ' + str(e)
    
    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app