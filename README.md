# DMS-inc-CSC4910
## Project Description

This project builds a public, easy-to-use website that predicts culvert condition ratings (1–5) from user-provided attributes (e.g., material, shape, age, environment) and returns full probability distributions with explanations. Behind the scenes, an ensemble of vetted ML models selects the best predictor based on whatever inputs the user has (handles partial inputs via smart defaults/imputation) and reports both the most likely rating and its confidence, with visual XAI (e.g., SHAP) to show which factors drove the result. Students will implement a secure model serving (e.g., FastAPI), a lightweight UI (React or Streamlit), calibrated probabilities, and guardrails that flag low-confidence or high-risk cases for human review. A pilot evaluation will compare platform outputs to held-out field records and gather usability feedback from agency partners. The outcome is a deployable, open-access decision-support tool that helps DOTs and local agencies prioritize inspections, reduce costs, and improve safety—while giving students portfolio-ready experience in applied AI, MLOps, and human-centered design.

---

## Documents
 - [Team Charter](https://docs.google.com/document/d/149NgPigSCGIX7yueF8f0Pnu0fES1BcW7ZFphQcvbJkk/edit?usp=sharing)
 - [Requirements Document](https://docs.google.com/document/d/1EEfwas8moUHnBnlsdQN27V9cU-uG57uX3xUNHZQ0Z0c/edit?usp=sharing)
