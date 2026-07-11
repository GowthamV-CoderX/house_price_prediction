from flask import Flask,jsonify,request,render_template
import pickle


app = Flask(__name__)

# load our model
linear_regression_model = pickle.load(open('models/house_price_model.pkl','rb'))
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictprice',methods=["POST"])
def predictprice():
    area = float(request.form["area"])
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    stories = int(request.form["stories"])

    mainroad = int(request.form["mainroad"])
    guestroom = int(request.form["guestroom"])
    basement = int(request.form["basement"])
    hotwaterheating = int(request.form["hotwaterheating"])
    airconditioning = int(request.form["airconditioning"])

    parking = int(request.form["parking"])
    prefarea = int(request.form["prefarea"])

    furnished = int(request.form["furnished"])
    unfurnished = int(request.form["unfurnished"])


    features = [[
        area,
        bedrooms,
        bathrooms,
        stories,
        mainroad,
        guestroom,
        basement,
        hotwaterheating,
        airconditioning,
        parking,
        prefarea,
        furnished,
        unfurnished
    ]]


    prediction = linear_regression_model.predict(features)

    price = round(prediction[0], 2)


    return f"Predicted House Price: ₹ {price}"
    
if __name__ == "__main__":
    app.run(debug=True)