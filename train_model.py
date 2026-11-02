import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re

# Load the dataset
dataset = pd.read_csv('dataset.csv')  # Replace with your actual file path

# Feature Engineering
dataset['url_length'] = dataset['url'].apply(len)
dataset['num_dots'] = dataset['url'].apply(lambda x: x.count('.'))
special_characters = r"[@_\-?&=]"
dataset['num_special_chars'] = dataset['url'].apply(lambda x: len(re.findall(special_characters, x)))
dataset['http_https'] = dataset['url'].apply(lambda x: 1 if x.startswith('http') else 0)
dataset['num_digits'] = dataset['url'].apply(lambda x: len(re.findall(r'\d', x)))

# Label Encoding
label_encoder = LabelEncoder()
dataset['type_encoded'] = label_encoder.fit_transform(dataset['type'])

# Features and labels
X = dataset[['url_length', 'num_dots', 'num_special_chars', 'http_https', 'num_digits']]
y = dataset['type_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save the model and label encoder
joblib.dump(model, 'suspicious_link_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
