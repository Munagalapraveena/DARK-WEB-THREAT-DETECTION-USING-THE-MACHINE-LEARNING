import streamlit as st
import joblib
import re
import base64

# Load the trained model and label encoder
model = joblib.load('suspicious_link_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Function to extract features from URL
def extract_features(url):
    url_length = len(url)
    num_dots = url.count('.')
    special_characters = r"[@_\-?&=]"
    num_special_chars = len(re.findall(special_characters, url))
    http_https = 1 if url.startswith('http') else 0
    num_digits = len(re.findall(r'\d', url))
    return [url_length, num_dots, num_special_chars, http_https, num_digits]

# Function to validate URL
def is_valid_url(url):
    url_regex = re.compile(
        r'^(https?://)?'  # optional http:// or https://
        r'([a-zA-Z0-9.-]+)'  # domain name or IP address
        r'(\.[a-zA-Z]{2,})'  # dot-something
        r'(/[-a-zA-Z0-9()@:%_\+.~#?&//=]*)?$'  # optional resource path
    )
    return re.match(url_regex, url) is not None

# Function for authentication
def login(username, password):
    if username == "admin" and password == "password123":
        return True
    return False

# Function to load and encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load the images and encode them
login_background = get_base64_of_bin_file('D:/Asan/falsewebsite/pexels-mati-5952651.jpg')
main_background = get_base64_of_bin_file('D:/Asan/falsewebsite/pexels-tima-miroshnichenko-5380665.jpg')

# Check authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Set background image based on authentication
background_image = login_background if not st.session_state.authenticated else main_background

# Streamlit app interface
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{background_image}");
        background-size: cover;
        background-position: center;
    }}
    .main-title {{
        font-size: 36px;
        color: #ffffff;
        text-align: center;
    }}
    .sub-title {{
        font-size: 20px;
        color: #dddddd;
        text-align: center;
        margin-bottom: 20px;
    }}
    .url-input {{
        text-align: center;
    }}
    .prediction-button {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }}
    .prediction-result {{
        font-size: 24px;
        font-weight: bold;
        color: #FF6347;
        text-align: center;
        margin-top: 20px;
    }}
    .explanation {{
        font-size: 16px;
        color: #ffffff;
        text-align: center;
        margin-top: 10px;
    }}
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 2px solid #cccccc;
        font-size: 16px;
        padding: 10px;
    }}
    .login-title {{
        font-size: 28px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
    }}
    .login-box {{
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
    }}
    .login-input {{
        width: 300px;
        margin-bottom: 10px;
    }}
    .stAlert > div {{
        background-color: #000000;
        color: #4CAF50;
        font-size: 18px;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Login Page
if not st.session_state.authenticated:
    st.markdown('<div class="main-title">Suspicious Link Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
    
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")
else:
    # Main App after login
    st.markdown('<div class="main-title">Suspicious Link Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Enter a URL to check if it is suspicious</div>', unsafe_allow_html=True)

    url_input = st.text_input("", placeholder="Enter the URL here", key="url_input", help="Input the URL you want to check.")

    if st.button("Predict", key="predict_button"):
        if is_valid_url(url_input):
            features = extract_features(url_input)
            prediction = model.predict([features])[0]
            prediction_label = label_encoder.inverse_transform([prediction])[0]

            result_message = f"The URL is predicted to be: {prediction_label}"
            explanation = ""
            if prediction_label == "benign":
                result_color = "#4CAF50"  # Green for benign
                explanation = "This URL appears to be safe based on its features."
            else:
                result_color = "#FF6347"  # Red for suspicious
                explanation = "This URL exhibits characteristics typical of suspicious links. Please be cautious."

            st.markdown(f'<div class="prediction-result" style="color:{result_color};">{result_message}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="explanation">{explanation}</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a valid URL.")
