import streamlit as st
from PIL import Image
import base64
from io import BytesIO

from model_helper import predict

# Streamlit page config
st.set_page_config(page_title="Car Damage Detection", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background: #e8eae8;
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    header, footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)




# Title
st.markdown("""
    <style>
        .title {
            font-size: 30px;
            font-weight: bold;
            color: #004488;
            text-align: center;
            margin-top: -40px;
        }

        .thumbnail {
            max-height: 27vh;
            border-radius: 8px;
            cursor: pointer;
            transition: 0.8s ease;
        }

        .thumbnail:hover {
            opacity: 0.85;
        }

        /* Fullscreen overlay */
        .overlay {
            position: fixed;
            display: none;
            justify-content: center;
            align-items: center;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0.2,0.8,0.6,0.95);
            z-index: 9999;
        }

        .overlay img {
            max-width: 80vw;
            max-height: 80vh;
            border-radius: 10px;
        }

        .overlay:target {
            display: flex;
        }

        .close-btn {
            position: absolute;
            top: 50px;
            right: 30px;
            font-size: 36px;
            color: #fff;
            text-decoration: none;
            z-index: 10000;
        }

        .result {
            margin-top: 10px;
            font-size: 30px;
            font-weight: 500;
            text-align: center;
            margin-bottom:-60px;
            background: #eef2f2;
            border-radius:16px;
        }
    </style>

    <div class="title">🚘 Car Damage Detection</div>
""", unsafe_allow_html=True)

# Upload section
uploaded_file = st.file_uploader("Upload a car image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    car_condition=predict(image)

    # Convert image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Display thumbnail with full-screen modal and close button
    html_image = f"""
        <a href="#img-modal">
            <img src="data:image/png;base64,{img_str}" class="thumbnail" alt="Uploaded Image"/>
        </a>

        <div id="img-modal" class="overlay">
            <a href="#" class="close-btn">✖</a>
            <img src="data:image/png;base64,{img_str}" alt="Full Image"/>
        </div>
    """
    st.markdown(html_image, unsafe_allow_html=True)

    st.markdown("<div style='padding-top: 10px'></div>", unsafe_allow_html=True)
    if st.button("🔍 Predict"):
        car_condition=predict(image)
        st.markdown(f'<div class="result">Car Condition : <b>{car_condition}</b>.</div>', unsafe_allow_html=True)

else:
    st.info("📤 Please upload an image to begin prediction.")
