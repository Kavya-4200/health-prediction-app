from sklearn.tree import DecisionTreeClassifier
import numpy as np


# Training Dataset
# Features:
# Glucose, Hemoglobin, Cholesterol

X = np.array([
    [90, 14, 180],
    [100, 13.5, 190],
    [110, 13, 200],
    [120, 13, 210],

    [140, 12, 220],
    [150, 11.5, 230],
    [160, 11, 240],

    [170, 10.5, 250],
    [180, 10, 260],
    [190, 9.5, 280]
])


# Output labels
y = [
    "Low Risk",
    "Low Risk",
    "Low Risk",
    "Low Risk",

    "Medium Risk",
    "Medium Risk",
    "Medium Risk",

    "High Risk",
    "High Risk",
    "High Risk"
]


# Create ML Model

model = DecisionTreeClassifier(
    random_state=42
)


# Train model

model.fit(X, y)



def predict_health(glucose, hemoglobin, cholesterol):

    result = model.predict(
        [
            [
                glucose,
                hemoglobin,
                cholesterol
            ]
        ]
    )

    return result[0]



def generate_remark(risk):

    if risk == "High Risk":

        return (
            "High health risk detected. "
            "Patient should consult a healthcare professional."
        )


    elif risk == "Medium Risk":

        return (
            "Moderate health risk detected. "
            "Regular monitoring is recommended."
        )


    else:

        return (
            "Low risk detected. "
            "Health indicators appear normal."
        )