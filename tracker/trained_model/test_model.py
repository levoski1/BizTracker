

import joblib
import pandas as pd
import re
from nltk.corpus import stopwords

# Load the trained model and vectorizer
best_model = joblib.load('logistic_regression_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Load stop words
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

# Provide the name of the new data file
new_data_file = 'new_data.csv'  # Change this to the name of your file

# Load new data from the file
new_data_df = pd.read_csv(new_data_file)

# Ensure the new data has a 'text' column
if 'text' not in new_data_df.columns:
    raise ValueError("The input file must contain a 'text' column")

# Preprocess the new input text
new_data_df['cleaned_text'] = new_data_df['text'].apply(preprocess_text)

# Vectorize the preprocessed text
new_texts_vec = vectorizer.transform(new_data_df['cleaned_text'])

# Make predictions
new_predictions = best_model.predict(new_texts_vec)

# Add predictions to the DataFrame
new_data_df['predicted_label'] = new_predictions

# Print or save the results
output_file = 'predictions.csv'  # Change this to your desired output file
new_data_df.to_csv(output_file, index=False)

print("Predictions saved to", output_file)


