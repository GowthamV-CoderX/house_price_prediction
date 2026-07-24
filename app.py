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

    errors = []


    # Area validation
    area = request.form["area"]

    if area == "":
        errors.append("Area is required.")

    else:
        try:
            area = float(area)

            if area <= 0:
                errors.append("Area must be greater than 0.")
            if area >= 10000:
                errors.append("Area must be in range of 0 - 10,000 Sq.ft")

        except ValueError:
            errors.append("Area must contain only numbers.")



    # Bedrooms validation
    bedrooms = request.form["bedrooms"]

    if bedrooms == "":
        errors.append("Bedrooms is required.")

    else:
        try:
            bedrooms = int(bedrooms)

            if bedrooms <= 0:
                errors.append("Bedrooms must be greater than 0.")
            if bedrooms >= 20:
                errors.append("Bedrooms must be in range of 0 - 20")
            if type(bedrooms) == float:
                errors.append("Bedrooms cannot be decimal must be in integer value")

        except ValueError:
            errors.append("Bedrooms must be an integer.")



    # Bathrooms validation
    bathrooms = request.form["bathrooms"]

    if bathrooms == "":
        errors.append("Bathrooms is required.")

    else:
        try:
            bathrooms = int(bathrooms)

            if bathrooms <= 0:
                errors.append("Bathrooms must be greater than 0.")
            
            if bathrooms > 20:
                errors.append("Bathrooms must be in range of 0 - 20")
            
            if type(bathrooms) == float:
                errors.append("bathrooms cannot be decimal must be in integer value")

        except ValueError:
            errors.append("Bathrooms must be an integer.")



    # Stories validation
    stories = request.form["stories"]

    if stories == "":
        errors.append("Stories are required.")
    else:
        try:
            stories = int(stories)
            if stories < 1 or stories > 10:
                errors.append("Stories must be between 1 and 4.")
            if type(stories) == float:
                errors.append("Stories cannot be decimal must be in integer value")
        except ValueError:
            errors.append("Stories must be an integer.")

    # Parking validation
    parking = request.form["parking"]
    if parking == "":
        errors.append("Parking is required.")
    else:
        try:
            parking = int(parking)
            if parking < 0 or parking > 5:
                errors.append("Parking must be between 0 and 3.")
            if type(parking) == float:
                errors.append("Parking cannot be decimal must be in integer value")
        except ValueError:
            errors.append("Parking must be an integer.")

    # If errors exist
    if errors:

        return render_template(
            "error.html",
            errors=errors
        )



    # remaining categorical values

    mainroad = int(request.form["mainroad"])
    guestroom = int(request.form["guestroom"])
    basement = int(request.form["basement"])
    hotwaterheating = int(request.form["hotwaterheating"])
    airconditioning = int(request.form["airconditioning"])
    prefarea = int(request.form["prefarea"])
    furnishing_status = request.form["furnishingstatus"]
    if furnishing_status == "furnished":
        furnished = 1
        unfurnished = 0

    elif furnishing_status == "unfurnished":
        furnished = 0
        unfurnished = 1

    else:  # Semi-Furnished
        furnished = 0
        unfurnished = 0



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

    price = round(prediction[0],2)


    return render_template(
    "prediction.html",
    prediction=round(prediction[0],2)
    )
    
if __name__ == "__main__":
    app.run(debug=True)