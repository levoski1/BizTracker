import joblib
import re
from nltk.corpus import stopwords

# Load the TF-IDF vectorizer and the Logistic Regression model
vectorizer_path = 'tracker/trained_model/tfidf_vectorizer.pkl'
model_path = 'tracker/trained_model/logistic_regression_model.pkl'

tfidf_vectorizer = joblib.load(vectorizer_path)
logistic_regression_model = joblib.load(model_path)

stop_words = set(stopwords.words('english'))

# Set a confidence threshold
confidence_threshold = 0.6

def predict_category(text):
    '''
    Create a function to make predictions
    Step 1: Transform the input text using the TF-IDF vectorizer
    Step 2: Use the logistic regression model to make a prediction
    Step 3: Return the prediction if confidence is above the threshold; otherwise, return an empty string
    '''
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    
    transformed_text = tfidf_vectorizer.transform([text])
    
    # Get prediction probabilities
    probabilities = logistic_regression_model.predict_proba(transformed_text)[0]
    max_prob = max(probabilities)
    
    # Check if the maximum probability is above the threshold
    if max_prob >= confidence_threshold:
        prediction = logistic_regression_model.classes_[probabilities.argmax()]
    else:
        prediction = ''
    
    return prediction





def preprocess_money(text):
    '''
    Extracts and returns the monetary value from the text if it is confirmed as a monetary value.
    Otherwise, returns an empty string.
    '''

    # Regular expression to match monetary amounts with currency symbols or names
    pattern = r'(\b(?:dollar|naira|euro|pound|yen|rupee)\s*\d+(?:\.\d{2})?)|([#\$€£]\s?\d+(?:\.\d{2})?)|\b\d+(?:\.\d{2})?\b'
    
    # Find all matches
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    if matches:
        amounts = []
        for match in matches:
            # Flatten the tuple and clean the match
            match = ''.join(match).strip()
            if match:
                # Remove currency names if present
                cleaned_match = re.sub(r'\b(?:dollar|naira|euro|pound|yen|rupee)\b', '', match, flags=re.IGNORECASE).strip()
                # Remove currency symbols
                cleaned_match = cleaned_match.replace('#', '').replace('$', '').replace('€', '').replace('£', '')
                try:
                    # Convert to float and append to amounts list
                    amount = float(cleaned_match)
                    amounts.append(amount)
                except ValueError:
                    continue
        
        # Return the largest amount rounded to 2 decimal places
        if amounts:
            return "{:.2f}".format(max(amounts))  # Ensure 2 decimal places
    
    return ''



