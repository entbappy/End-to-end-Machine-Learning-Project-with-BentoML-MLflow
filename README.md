# Network-Security-with-Machine-Learning

In this data science project, you will build a machine learning system which will be able predict whether the website is phising or not. This project will be very usefull for cyber security domain where spam or malicious websites can be sorted based on the certain indicators. As we know that internet is getting very accessible to everyone by the day, in the similar rate spam or malicious website who cheated people or cause fraud to lot of people, so search engine companies like Google, Microsoft, Brave, etc have to detect a block such website, the end user does not land up in the malicious website, we can also consider like the feature of safe search in Google Chrome or similar search engines. 

Since the number of websites in the internet, very very huge and increasing a lot faster pace, these companies have to problem of keeping track of these kind of websites and block them. So in order to solve these issues, we can use machine learning techniques to analyze patterns in malicious website and through some cyber security domain knowledge, we can build a machine learning system, to predict whether a particular website is malicious or not.

## Tech Stack Used

1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
%. MongoDB

## How to run?

Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage.

### Step 1: Clone the repository

```bash
git clone https://github.com/sethusaim/Network-Security-with-Machine-Learning.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n network python=3.7.6 -y
```

```bash
conda activate network
```

### Step 3 - Install the requirements

```bash
pip install -r requirements.txt
```

### Step 4 - Export the MongoDB URL environment variable

```bash
export MONGODB_URL="mongodb://localhost:27017"
```

### Step 5 - Run the application server

```bash
python app.py
```
