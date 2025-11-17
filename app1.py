import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import base64

# ================================================================
#                      PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Crop Disease Detector",
    page_icon="🌿",
    layout="centered"
)
# ================================================================
bg_url = "https://thumbs.dreamstime.com/b/smart-farming-precision-agriculture-technology-young-plants-growing-soil-image-showcases-thriving-rich-overlaid-futuristic-379525081.jpg"



# ================================================================
#                      GLOBAL STYLING (CSS)
# ================================================================
st.markdown("""
    <style>
    
    /* ---------- GLOBAL BACKGROUND (Sky Blue Theme) ----------- */
    .stApp {
        background: linear-gradient(135deg, #b3e5fc 0%, #81d4fa 50%, #4fc3f7 100%);
        background-attachment: fixed;
    }

    /* ---------- MAIN TITLE ---------- */
    h1 {
        text-align: center;
        color: #01579b;
        font-size: 50px !important;
        font-weight: 900;
        text-shadow: 2px 2px 5px #000000;
        margin-bottom: 10px;
    }

    /* ---------- Subtitle ---------- */
    .subheader {
        color: #0277bd;
        text-align: center;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 25px;
    }

    /* ---------- Uploaded Image Styling ---------- */
    .uploaded-img {
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        margin-bottom: 20px;
        border: 4px solid #4fc3f7;
    }
    /* Stylish uploaded image */
.uploaded-img {
    width: 360px !important;
    border-radius: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.30);
    border: 4px solid rgba(255,255,255,0.5);

    /* Light glass effect */
    backdrop-filter: blur(8px);
    background: rgba(255,255,255,0.15);

    transition: 0.35s ease-in-out;
}

/* Hover Zoom Effect */
.uploaded-img:hover {
    transform: scale(1.07);
    box-shadow: 0 15px 35px rgba(0,0,0,0.45);
    border-color: rgba(255,255,255,0.8);
}


    /* ---------- Prediction Card ---------- */
    .result-box {
        background: #e1f5fe;
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        border-left: 10px solid #0288d1;
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
        margin-top: 25px;
    }

    .result-box h2 {
        color: #01579b;
        font-weight: 800;
    }

    .result-box h3 {
        color: #0277bd;
        font-size: 26px;
        font-weight: 700;
    }

    /* ---------- Solution Box ---------- */
    .solution-box {
        background: #f0fbff;
        padding: 25px;
        border-left: 10px solid #039be5;
        border-radius: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        margin-top: 25px;
        font-size: 17px;
        color: #004c6d;
    }

    /* ---------- File Uploader Center ---------- */
    .css-10trblm {
        margin-left: auto;
        margin-right: auto;
    }

    /* ---------- Buttons ---------- */
    .stButton>button {
        background: #0288d1;
        color: white;
        padding: 12px 30px;
        font-size: 20px;
        font-weight: 700;
        border-radius: 15px;
        border: none;
        box-shadow: 0px 6px 12px rgba(0,0,0,0.25);
        cursor: pointer;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #01579b;
        transform: scale(1.08);
    }

    </style>
""", unsafe_allow_html=True)


# ================================================================
#                      LOAD MODEL
# ================================================================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("1.keras")

model = load_model()

# ================================================================
#                      CLASS LABELS
# ================================================================
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
    'Tomato___healthy'
]

# ================================================================
#                      SOLUTIONS (from earlier message)
# ================================================================
# 👉 Yaha wahi solutions paste karna jo maine tumhe upar diye hain
# from solutions_data import solutions  # (Optional external file support)
solutions = {

    # --------------------- APPLE ---------------------
    'Apple___Apple_scab': """
        ### 🍏 Apple Scab – Solution
        - Fungicide spray (Mancozeb / Captan)
        - Prune infected branches
        - Remove fallen leaves
        - Ensure proper air circulation
    """,

    'Apple___Black_rot': """
        ### 🍎 Apple Black Rot – Solution
        - Remove and destroy infected fruits & twigs
        - Apply copper-based fungicide
        - Maintain orchard cleanliness
    """,

    'Apple___Cedar_apple_rust': """
        ### 🍎 Cedar Apple Rust – Solution
        - Apply preventive fungicides (Myclobutanil)
        - Remove nearby juniper trees if possible
        - Improve airflow between trees
    """,

    'Apple___healthy': """
        ### 🍏 Healthy Apple Plant
        - Maintain regular irrigation
        - Keep checking for early symptoms
        - Use organic fertilizers
    """,

    # --------------------- BLUEBERRY ---------------------
    'Blueberry___healthy': """
        ### 🫐 Healthy Blueberry Plant
        Everything looks good! Keep the soil acidic (pH 5.0) and avoid waterlogging.
    """,

    # --------------------- CHERRY ---------------------
    'Cherry_(including_sour)___Powdery_mildew': """
        ### 🍒 Powdery Mildew (Cherry)
        - Use sulfur or neem oil
        - Remove infected leaves
        - Avoid overhead watering
    """,

    'Cherry_(including_sour)___healthy': """
        ### 🍒 Healthy Cherry Plant
        Keep the tree pruned and maintain good soil moisture.
    """,

    # --------------------- CORN ---------------------
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': """
        ### 🌽 Gray Leaf Spot – Solution
        - Rotate crops
        - Apply fungicide (Azoxystrobin)
        - Avoid dense plantation
    """,

    'Corn_(maize)___Common_rust_': """
        ### 🌽 Common Rust – Solution
        - Use resistant hybrids
        - Apply fungicide (Propiconazole)
        - Remove affected leaves
    """,

    'Corn_(maize)___Northern_Leaf_Blight': """
        ### 🌽 Northern Leaf Blight – Solution
        - Fungicide spray at early stages
        - Crop rotation
        - Improve field drainage
    """,

    'Corn_(maize)___healthy': """
        ### 🌽 Healthy Corn
        Keep monitoring moisture levels and avoid waterlogging.
    """,

    # --------------------- GRAPES ---------------------
    'Grape___Black_rot': """
        ### 🍇 Black Rot – Solution
        - Remove mummified berries
        - Spray Mancozeb or Captan
        - Increase sunlight exposure
    """,

    'Grape___Esca_(Black_Measles)': """
        ### 🍇 Black Measles – Solution
        - Prune infected vines
        - Avoid vine stress
        - Use fungicide during early growth
    """,

    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': """
        ### 🍇 Leaf Blight – Solution
        - Copper fungicide is effective
        - Remove diseased leaves
        - Maintain proper vine spacing
    """,

    'Grape___healthy': """
        ### 🍇 Healthy Grape Plant
        Keep proper irrigation and pruning cycle.
    """,

    # --------------------- ORANGE ---------------------
    'Orange___Haunglongbing_(Citrus_greening)': """
        ### 🍊 Citrus Greening – Solution
        - No complete cure exists
        - Remove infected branches
        - Control psyllid insects with insecticide
        - Use resistant varieties
    """,

    # --------------------- PEACH ---------------------
    'Peach___Bacterial_spot': """
        ### 🍑 Bacterial Spot – Solution
        - Apply copper spray
        - Use disease-free seeds
        - Improve air circulation
    """,

    'Peach___healthy': """
        ### 🍑 Healthy Peach Plant
        Keep monitoring and follow seasonal pruning.
    """,

    # --------------------- PEPPER ---------------------
    'Pepper,_bell___Bacterial_spot': """
        ### 🌶 Bell Pepper Bacterial Spot – Solution
        - Copper-based fungicide
        - Remove infected leaves
        - Use drip irrigation
    """,

    'Pepper,_bell___healthy': """
        ### 🌶 Healthy Pepper Plant
        Maintain good drainage and check leaves regularly.
    """,

    # --------------------- POTATO ---------------------
    'Potato___Early_blight': """
        ### 🥔 Early Blight – Solution
        - Apply Mancozeb or Chlorothalonil
        - Avoid overhead irrigation
        - Remove infected leaves
    """,

    'Potato___Late_blight': """
        ### 🥔 Late Blight – Solution
        - Use copper fungicide immediately
        - Destroy severely infected plants
        - Improve airflow and reduce humidity
    """,

    'Potato___healthy': """
        ### 🥔 Healthy Potato Plant
        Continue normal irrigation and pest control.
    """,

    # --------------------- RASPBERRY ---------------------
    'Raspberry___healthy': """
        ### Healthy Raspberry Plant
        Mulch properly and prevent fungal infections.
    """,

    # --------------------- SOYBEAN ---------------------
    'Soybean___healthy': """
        ### Healthy Soybean Plant
        Maintain soil nutrients and avoid overwatering.
    """,

    # --------------------- SQUASH ---------------------
    'Squash___Powdery_mildew': """
        ### 🎃 Powdery Mildew – Solution
        - Spray neem oil
        - Provide sun exposure
        - Use resistant varieties
    """,

    # --------------------- STRAWBERRY ---------------------
    'Strawberry___Leaf_scorch': """
        ### 🍓 Leaf Scorch – Solution
        - Remove burnt leaves
        - Maintain soil moisture
        - Avoid direct hot sunlight
    """,

    'Strawberry___healthy': """
        ### 🍓 Healthy Strawberry Plant
        Provide good mulching and irrigation.
    """,

    # --------------------- TOMATO ---------------------
    'Tomato___Bacterial_spot': """
        ### 🍅 Bacterial Spot – Solution
        - Use copper spray
        - Remove diseased leaves
        - Avoid leaf wetting
    """,

    'Tomato___Early_blight': """
        ### 🍅 Early Blight – Solution
        - Apply Chlorothalonil
        - Improve ventilation
        - Remove infected foliage
    """,

    'Tomato___Late_blight': """
        ### 🍅 Late Blight – Solution
        - Destroy infected plants
        - Apply copper fungicide
        - Reduce field humidity
    """,

    'Tomato___Leaf_Mold': """
        ### 🍅 Leaf Mold – Solution
        - Maintain airflow
        - Use sulfur-based fungicide
        - Avoid overcrowding of plants
    """,

    'Tomato___Septoria_leaf_spot': """
        ### 🍅 Septoria Leaf Spot – Solution
        - Prune lower leaves
        - Copper fungicide spray
        - Water plants at soil level
    """,

    'Tomato___Spider_mites Two-spotted_spider_mite': """
        ### 🕷 Tomato Spider Mites – Solution
        - Spray neem oil
        - Increase humidity
        - Wash leaves with water
    """,

    'Tomato___Target_Spot': """
        ### 🍅 Tomato Target Spot – Solution
        - Use Mancozeb fungicide
        - Remove old leaves
        - Maintain spacing
    """,

    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': """
        ### 🍅 TYLCV – Solution
        - Whitefly control is necessary
        - Use resistant tomato varieties
        - Remove infected plants
    """,

    'Tomato___Tomato_mosaic_virus': """
        ### 🍅 Tomato Mosaic Virus – Solution
        - Wash hands after touching plants
        - Remove infected plants
        - Disinfect tools
    """,

    'Tomato___healthy': """
        ### 🍅 Healthy Tomato Plant
        Regular watering, proper sunlight, and pruning recommended.
    """
}

# ================================================================
#                      MAIN TITLE
# ================================================================
st.markdown("<h1>CROP DISEASE PREDICTION SYSTEM</h1>", unsafe_allow_html=True)
st.write("### 🌿 Upload any crop leaf image to detect disease")

# ================================================================
#                      UPLOAD IMAGE
# ================================================================
uploaded_file = st.file_uploader("📤 Upload Leaf Image", type=["jpg", "jpeg", "png"])

if uploaded_file:

    image = Image.open(uploaded_file)
    st.markdown("<img src='data:image/png;base64," 
            + base64.b64encode(uploaded_file.getvalue()).decode() 
            + "' class='uploaded-img'/>",
            unsafe_allow_html=True)


    # Preprocessing
    img = image.resize((256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)

    # Prediction
    preds = model.predict(img_array)
    idx = np.argmax(preds[0])
    pred_class = class_names[idx]
    confidence = float(np.max(preds[0]) * 100)

    # ================================================================
    #                RESULT - BEAUTIFUL CARD
    # ================================================================
    st.markdown(f"""
        <div class="result-box">
            <h2>🌱 Prediction Result</h2>
            <h3><b>{pred_class}</b></h3>
            <p style="font-size:22px; color:#2b4c7e;">
                Confidence: <b>{confidence:.2f}%</b>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ================================================================
    #                SOLUTION - STYLED BOX
    # ================================================================
    solution_text = solutions.get(pred_class, "No solution available for this disease yet.")

    st.markdown(f"""
        <div class="solution-box">
            <h3>🛠 Recommended Treatment</h3>
            {solution_text}
        </div>
    """, unsafe_allow_html=True)
