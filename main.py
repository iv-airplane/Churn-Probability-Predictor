import gradio as gr
import pandas as pd
import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator
from typing import Literal
from utilities import FEATURES_CONFIG, FEATURE_NAMES, MARKDOWN_DESC, TECHNICAL_DESC

app = FastAPI(
    title="Telco Churn Prediction API",
    description="Deployment.",
    version="1.0.0"
)

# --- Load the trained model ---
model = joblib.load("churn_pipeline.joblib")


#  Define the Input Schema
class ChurnInput(BaseModel):
    gender: Literal["Female", "Male"]
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int = Field(ge=0, description="Months the customer has stayed")
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["No phone service", "No", "Yes"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["No", "Yes", "No internet service"]
    OnlineBackup: Literal["No", "Yes", "No internet service"]
    DeviceProtection: Literal["No", "Yes", "No internet service"]
    TechSupport: Literal["No", "Yes", "No internet service"]
    StreamingTV: Literal["No", "Yes", "No internet service"]
    StreamingMovies: Literal["No", "Yes", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: Literal["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
    MonthlyCharges: float = Field(gt=0)
    TotalCharges: float = Field(ge=0)

    @model_validator(mode='after')
    def check_consistent_charges(self) -> 'ChurnInput':
        if self.TotalCharges < self.MonthlyCharges:
            raise ValueError(
                f"TotalCharges ({self.TotalCharges}) cannot be less than MonthlyCharges ({self.MonthlyCharges}).")
        return self

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "gender": "Female",
                "SeniorCitizen": 1,
                "Partner": "No",
                "Dependents": "No",
                "tenure": 1,
                "PhoneService": "Yes",
                "MultipleLines": "No",
                "InternetService": "Fiber optic",
                "OnlineSecurity": "No",
                "OnlineBackup": "No",
                "DeviceProtection": "No",
                "TechSupport": "No",
                "StreamingTV": "Yes",
                "StreamingMovies": "Yes",
                "Contract": "Month-to-month",
                "PaperlessBilling": "Yes",
                "PaymentMethod": "Electronic check",
                "MonthlyCharges": 105.65,
                "TotalCharges": 105.65
            }
        }

def compute_prediction(data_dict: dict):
    """Handles the prediction logic, calls a trained model."""
    validated_data = ChurnInput(**data_dict)

    # Convert data into df for Scikit-learn Pipeline
    df = pd.DataFrame([validated_data.model_dump()])

    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]

    return prediction, prob

@app.post("/predict")
def predict_api(payload: ChurnInput):
    """An API Endpoint to integrate FastAPI and Gradio"""
    prediction, prob = compute_prediction(payload.model_dump())
    return {
        "is_churner": bool(prediction),
        "churn_probability": float(prob),
        "risk_level": "High" if prediction == 1 else "Low"
    }

def gradio_ui_launcher(*args):
    """
    Connects UI components to the backend orchestration.
    """
    try:
        # Create a dictionary by zipping names and values
        input_dict = dict(zip(FEATURE_NAMES, args))

        # Obtain the prediction
        prediction, prob = compute_prediction(input_dict)

        return f"Prediction: {'Churn' if prob > 0.5 else 'Stay'} (Churning Probability: {prob:.2%})"
    except Exception as e:
        # Catches Pydantic validation errors and displays
        # them in a textbox.
        return f"⚠️ Input Error: {str(e)}"

# --- UI DESIGN ---
def create_component(feat):
    """Generates Gradio components based on a configuration"""
    if feat["type"] == "dropdown":
        return gr.Dropdown(choices=feat["options"], label=feat["name"], value=feat["default"])
    elif feat["type"] == "radio":
        return gr.Radio(choices=feat["options"], label=feat["name"], value=feat["default"])
    elif feat["type"] == "slider":
        return gr.Slider(minimum=feat["min"], maximum=feat["max"], label=feat["name"], value=feat["default"])
    elif feat["type"] == "checkbox":
        return gr.Checkbox(label=feat["name"], value=feat["default"])
    elif feat["type"] == "number":
        return gr.Number(label=feat["name"], value=feat["default"])

inputs = []

with gr.Blocks(title="Telco Churn Dashboard") as demo:
    gr.Markdown(MARKDOWN_DESC)

    with gr.Row():
        # --- LEFT COLUMN: INPUTS (Scale 2 = takes up 66% width) ---
        with gr.Column(scale=2):
            with gr.Tabs():

                # Tab 1: Profile
                with gr.Tab("👤 Profile"):
                    gr.Markdown("### Demographic Details")
                    # Loop through first 7 features
                    for feat in FEATURES_CONFIG[:7]:
                        comp = create_component(feat)
                        inputs.append(comp)  # Add to global list

                # Tab 2: Services
                with gr.Tab("📡 Services"):
                    gr.Markdown("### Subscribed Services")
                    # Loop through next 7 features
                    for feat in FEATURES_CONFIG[7:14]:
                        comp = create_component(feat)
                        inputs.append(comp)

                # Tab 3: Billing
                with gr.Tab("💳 Billing"):
                    gr.Markdown("### Contract & Payment")
                    # Loop through remaining features
                    for feat in FEATURES_CONFIG[14:]:
                        comp = create_component(feat)
                        inputs.append(comp)

                with gr.Tab("⚙️ How it works?"):
                    gr.Markdown(TECHNICAL_DESC)

        # --- RIGHT COLUMN: OUTPUT (Scale 1 = takes up 33% width) ---
        with gr.Column(scale=1):
            gr.Markdown("### 📊 Live Analysis")

            # Stays visible no matter which tab is selected on the left.
            output_box = gr.Textbox(label="Churn Risk Prediction", lines=4)

            analyze_btn = gr.Button("RUN ANALYSIS", variant="primary", size="lg")

            gr.Markdown("""
            **Interpretation Guide:**
            * 🟢 **Low Risk:** < 50%
            * 🔴 **High Risk:** > 50%
            """)

    # --- THE LINKING ---
    # Even though inputs are in different tabs, we gather all inputs the master list 'all_inputs'
    # and pass it to the function.
    analyze_btn.click(
        fn=gradio_ui_launcher,
        inputs=inputs,
        outputs=output_box
    )

# Link the  FastAPI 'app' with the Gradio 'demo'
app = gr.mount_gradio_app(app, demo, path="/")