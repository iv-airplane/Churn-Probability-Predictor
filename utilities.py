FEATURES_CONFIG = [
    {"name": "gender", "type": "dropdown", "options": ["Female", "Male"], "default": "Female"},
    {"name": "SeniorCitizen", "type": "checkbox", "default": True},
    {"name": "Partner", "type": "radio", "options": ["Yes", "No"], "default": "No"},
    {"name": "Dependents", "type": "radio", "options": ["Yes", "No"], "default": "No"},
    {"name": "tenure", "type": "slider", "min": 0, "max": 72, "default": 1},
    {"name": "PhoneService", "type": "radio", "options": ["Yes", "No"], "default": "Yes"},
    {"name": "MultipleLines", "type": "dropdown", "options": ["No phone service", "No", "Yes"], "default": "No"},
    {"name": "InternetService", "type": "dropdown", "options": ["DSL", "Fiber optic", "No"], "default": "Fiber optic"},
    {"name": "OnlineSecurity", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "No"},
    {"name": "OnlineBackup", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "No"},
    {"name": "DeviceProtection", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "No"},
    {"name": "TechSupport", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "No"},
    {"name": "StreamingTV", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "Yes"},
    {"name": "StreamingMovies", "type": "dropdown", "options": ["No", "Yes", "No internet service"], "default": "Yes"},
    {"name": "Contract", "type": "dropdown", "options": ["Month-to-month", "One year", "Two year"], "default": "Month-to-month"},
    {"name": "PaperlessBilling", "type": "radio", "options": ["Yes", "No"], "default": "Yes"},
    {"name": "PaymentMethod", "type": "dropdown", "options": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"], "default": "Electronic check"},
    {"name": "MonthlyCharges", "type": "number", "default": 105.65},
    {"name": "TotalCharges", "type": "number", "default": 105.65},
]

# Extract names for the zip() mapping later
FEATURE_NAMES = [f["name"] for f in FEATURES_CONFIG]

MARKDOWN_DESC = """
# Churn Probability Predictor
This service predicts the likelihood of customer churn (service cancellation) using a machine learning pipeline. 
By adjusting inputs such as contract type, internet service, and monthly charges, you can see how each influences churn 
risk in real time. The fields are already pre-populated with data to indicate high churn probability.

Our model identifies risk based on 19 factors, but these **Top 5** most important ones:
1.  **Contract Type**: Month-to-month users are 5 times more likely to churn than those on long-term contracts.
2.  **InternetService**: Fiber optic customers are more likely to cancel service compared to other internet service users.
3.  **TechSupport**: Users with No tech support.
4.  **OnlineSecurity**: Users with No online security.
5.  **TotalCharges**: Customers with higher charges are more likely to churn.

For more technical details go to "How it works?" tab.
"""

TECHNICAL_DESC = """
## Overview
High-recall churn prediction service built using XGBoost and FastAPI.

## Architecture
- FastAPI backend for input validation and preprocessing
- Pre-trained XGBoost model for inference
- Schema enforcement and business logic checks

## Model
- Weighted XGBoost classifier.
- Optimized for recall (~82%) to minimize missed churners.
- 19 features capturing contract, services, and billing behavior.

## Data Validation
- Strict schema checks.
- Business constraints on monetary fields.

## Feature Importance
Top drivers include contract type, internet service, support availability, and total charges.

## Dataset
Trained on the Telco Customer Churn dataset:
<https://www.kaggle.com/datasets/blastchar/telco-customer-churn/data>
"""