# DMS-inc-CSC4910
## Project Description

This project develops a public, user-friendly website that predicts culvert condition ratings (1–5) based on user-provided attributes (e.g., material, shape, age, environment) and returns full probability distributions with accompanying explanations. Behind the scenes, an ensemble of vetted ML models selects the best predictor based on whatever inputs the user has (handles partial inputs via smart defaults/imputation). It reports both the most likely rating and its confidence, accompanied by visual XAI (e.g., SHAP) to illustrate which factors contributed to the result. Students will implement a secure model serving framework (e.g., FastAPI), a lightweight UI (such as React or Streamlit), calibrated probabilities, and guardrails that flag low-confidence or high-risk cases for human review. A pilot evaluation will compare platform outputs to held-out field records and gather usability feedback from agency partners. The outcome is a deployable, open-access decision-support tool that helps DOTs and local agencies prioritize inspections, reduce costs, and improve safety—while giving students portfolio-ready experience in applied AI, MLOps, and human-centered design.

---

## Installation / Usage

### Installation

- To setup the project run the following:
```bash
ant dist
```

- Run the server first is as follows:
```bash
java -jar dist/server.jar
```

- Run the client next as follows:
```bash
java -jar dist/client.jar
```


Here are the steps to get the website up and running on your own device so that all the features work the way that they are supposed to:

1. Getting the repo on your machine:
```bash
cd <directory_you_want_this_repo_in>
git repo clone <repo_url>
```

2. Set up your own API keys
   - For this, you will have to make your own Google OAuth API keys and put these in a file called api_key.py in the src directory of the project.
   - You will need to name them this CLIENT_ID = "your_client_id_from_google_oauth" and CLIENT_SECRET = "goodle_oauth_secret"
  
3. Set up the venv
   - This should be done in the directory of the project repo

Linux/MacOS
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Windows
```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```
   - These commands will help set up your venv so that it has all the needed libraries to run this project

4. Set up the database
   - Now we need to initialize the database and make sure that all the tables are added to it.
  
```bash
cd src
flask db init
flask db migrate
flask db upgrade
```
   - These commands only need to be run once

---

### Usage

Now all you need to do to run the website is run this while your venv is activated;
```bash
python src/run.py
```
Then click the link that you are given in the terminal.

---

## Documents
 - [Shared Drive](https://drive.google.com/drive/folders/1LtWyccoxI1UAKXgWFkr09b5TkA9GCpDp?usp=drive_link)
 - [Team Charter](https://docs.google.com/document/d/149NgPigSCGIX7yueF8f0Pnu0fES1BcW7ZFphQcvbJkk/edit?usp=sharing)
 - [Requirements Document](https://docs.google.com/document/d/1EEfwas8moUHnBnlsdQN27V9cU-uG57uX3xUNHZQ0Z0c/edit?usp=sharing)
 - [Function Spec Document](https://docs.google.com/document/d/1mNoZxIZMnMPij4--SMbyazGPRnZfoIoB1KvsgGCOcZU/edit?usp=sharing)
 - [Poster](https://www.canva.com/design/DAG5don9qN0/u5UHJOR2NZxa7aOnn9y5RQ/view?utm_content=DAG5don9qN0&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hfb71b60f78)
