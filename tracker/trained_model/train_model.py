
import nltk
nltk.download('stopwords')
import random
import pandas as pd
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import joblib

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Define the examples for each category
income_examples = [
    "received salary for the month", "income from side business", "sold old furniture", 
    "freelance project earnings", "sold stocks for profit", "salary increase this quarter", 
    "earnings from rental property", "monthly dividend received", "bonus for completed projects", 
    "investment interest income", "profit from sale of assets", "cashback from credit card", 
    "government subsidy received", "pension payment", "royalties from book sales", 
    "referral bonus", "tax refund received", "income from consulting", "gift from family", 
    "won a prize", "end-of-year bonus", "inheritance money", "selling homemade crafts", 
    "freelance writing payment", "side job income", "commission from sales", 
    "cash gift for birthday", "stock dividends", "affiliate marketing earnings", 
    "money from rent", "got paid for freelance work", "collected rental income", 
    "received a scholarship", "earned money from part-time work", "received business profit"
]

expenses_examples = [
    "bought groceries", "paid for car repair", "monthly rent payment", "dining out with friends", 
    "bought new shoes", "annual subscription fee", "dinner at a fancy restaurant", 
    "paid for internet service", "groceries for the week", "utility bill payment", 
    "car maintenance costs", "medical bills", "subscription renewal", "gym membership fee", 
    "clothing purchase", "vacation expenses", "entertainment costs", "gas bill payment", 
    "household repairs", "education expenses", "water bill", "electricity bill", 
    "new phone purchased", "charity donation", "furniture purchase", "insurance premium", 
    "movie tickets", "shopping for clothes", "travel expenses", "subscription to streaming service", 
    "pet care expenses", "paid rent", "bought airtime/data", "paid school fees", 
    "bought fuel", "spent on entertainment", "paid medical bills"
]

debt_examples = [
    "paid credit card bill", "loan repayment", "mortgage payment due", 
    "credit card debt accumulation", "settled personal loan", "paid off student loan", 
    "refinanced my mortgage", "car loan repayment", "student loan payment", 
    "debt consolidation payment", "paying off mortgage", "credit card interest", 
    "car financing payment", "personal loan repayment", "medical loan payment", 
    "home equity loan payment", "loan from bank", "debt repayment to family", 
    "consolidation loan payment", "loan for home renovation", "paying down line of credit", 
    "bridge loan payment", "vacation loan repayment", "loan for business startup", 
    "settling overdue bills", "finance agreement payment", "credit line repayment", 
    "loan installment payment", "emergency loan repayment", "short-term loan payment", 
    "paid back borrowed money", "settled overdraft fee", "paid business loan", 
    "paid back office advance", "paid debt to supplier"
]


# Function to create synthetic data
def create_synthetic_data(num_samples, income_examples, expenses_examples, debt_examples):
    data = {"text": [], "label": []}
    for _ in range(num_samples):
        category = random.choice(["INCOME", "EXPENSES", "DEBT"])
        if category == "INCOME":
            data["text"].append(random.choice(income_examples))
            data["label"].append("INCOME")
        elif category == "EXPENSES":
            data["text"].append(random.choice(expenses_examples))
            data["label"].append("EXPENSES")
        else:
            data["text"].append(random.choice(debt_examples))
            data["label"].append("DEBT")
    return data

# Create additional 1000 synthetic data points
additional_data = create_synthetic_data(1000, income_examples, expenses_examples, debt_examples)


# Combine synthetic data with any existing data
new_data = additional_data

# Convert to DataFrame
df = pd.DataFrame(new_data)

# Stop words setup
stop_words = set(stopwords.words('english'))

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

# Apply preprocessing
df['cleaned_text'] = df['text'].apply(preprocess_text)

# Split the data
X = df['cleaned_text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Balance the training data using SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train_vec, y_train)

# Hyperparameter tuning using Grid Search
parameters = {
    'C': [0.1, 1, 10, 100],
    'solver': ['newton-cg', 'lbfgs', 'liblinear']
}

model = LogisticRegression()
clf = GridSearchCV(model, parameters, cv=5, scoring='f1_weighted')
clf.fit(X_train_balanced, y_train_balanced)
best_model = clf.best_estimator_

# Train the best model
best_model.fit(X_train_balanced, y_train_balanced)

# Predict and evaluate
y_pred = best_model.predict(X_test_vec)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the trained model and vectorizer
joblib.dump(best_model, 'logistic_regression_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')


