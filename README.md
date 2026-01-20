# Churn-Probability-Predictor

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

## 🚀 Getting Started: Running Application Locally

Follow these instructions to get the Churn Probability Predictor running on your local machine.

### Prerequisites
Before you begin, ensure you have the following installed:
* **Git:** [Download here](https://git-scm.com/downloads)
* **Docker Desktop:** [Download here](https://www.docker.com/products/docker-desktop/)

**⚠️ Important:** You must have the **Docker Desktop app open and running** before executing any Docker commands in your terminal.

Please note that Docker might need some time to build an image.

---

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <your-github-repo-link-here>
   cd <your-repo-folder-name>
   ```

2. **Build the Docker Image (Ensure you include . at the end ot the command)**
    ```
    docker build -t telco-app .
    ```

3. **Run the container**
    ```
    docker run -p 7860:7860 --name telco-running telco-app
    ```

4. **Go to the demo (don't click the Docker link!). Instead, go directly to**
    ```
    http://localhost:7860/
    ```

5. **Remove the container when you are done**
    ```
    docker stop telco-running
    docker rm telco-running
    ```
6. **Close the Docker app**
