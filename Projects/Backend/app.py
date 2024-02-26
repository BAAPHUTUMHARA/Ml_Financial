from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__, static_folder='static')

# Load the serialized XGBoost model
xgb_model = joblib.load('Backend/xgb_model.pkl')


@app.route('/')
def index():
    return render_template('webpage2.html')

@app.route('/webpage1', methods=['GET', 'POST'])
def webpage1():
    if request.method == 'POST':
        # Retrieve the form data
        amount = float(request.form['amount'])
        oldbalanceOrg = float(request.form['oldbalanceOrg'])
        newbalanceOrig = float(request.form['newbalanceOrig'])
        oldbalanceDest = float(request.form['oldbalanceDest'])
        newbalanceDest = float(request.form['newbalanceDest'])
        
        # Create a DataFrame from the form data
        input_data = pd.DataFrame([[amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]], 
                                  columns=['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'])
        
        # Make prediction using the XGBoost model
        prediction = xgb_model.predict(input_data)
        
        # Determine the prediction result
        result = "Fraudulent Transaction" if prediction[0] == 1 else "Legitimate Transaction"
        
        # Pass the prediction result to the template
        return render_template('webpage1.html', prediction=result)
    
    # Render the webpage1.html template for GET requests
    return render_template('webpage1.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)