

import streamlit as st
from PIL import Image
from skin_analyzer import SkinAnalyzer
from datetime import datetime
import os
import glob

# Configuration de la page
st.set_page_config(
    page_title="SkinAnalyzer",
    page_icon="🔬",
    layout="wide"
)

# Styles CSS - Fond sombre, texte clair
st.markdown("""
<style>
    /* Fond principal sombre */
    .stApp {
        background-color: #1a1a2e;
    }
    
    /* Texte principal clair */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #cccccc;
        margin-bottom: 2rem;
        font-size: 1rem;
    }
    
    /* Métriques */
    .metric-blue {
        background: #0f3460;
        padding: 1rem;
        border-radius: 10px;
        color: #ffffff;
        text-align: center;
        border: 1px solid #16213e;
    }
    
    /* Sidebar sombre */
    [data-testid="stSidebar"] {
        background-color: #16213e;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    
    /* Messages */
    .message-success {
        background: #0a4a2e;
        color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00ff88;
    }
    
    .message-warning {
        background: #5c3a00;
        color: #ffd966;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffaa00;
    }
    
    .message-error {
        background: #5c1a1a;
        color: #ffaaaa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff3333;
    }
    
    /* Cartes images test */
    .test-card {
        background: #16213e;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #0f3460;
        margin: 0.5rem;
    }
    
    /* Texte général */
    .stMarkdown, .stText, label, .st-bb {
        color: #ffffff;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #0f3460;
    }
    
    /* Alertes et infos */
    .stAlert {
        background-color: #16213e;
        color: #ffffff;
    }
    
    /* Uploader */
    .uploadedFile {
        background-color: #16213e;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏥 À propos")
    st.markdown("**SkinAnalyzer** - MobileNetV3")
    
    st.markdown("---")
    st.markdown("### 📋 Conseils")
    st.markdown("- Lumière naturelle")
    st.markdown("- Zone bien visible")
    st.markdown("- Photo nette")
    
    st.markdown("---")
    if 'analysis_count' not in st.session_state:
        st.session_state.analysis_count = 0
    st.metric("📊 Analyses", st.session_state.analysis_count)

# Header
st.markdown('<div class="main-title">🔬 SkinAnalyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyse de problèmes de peau</div>', unsafe_allow_html=True)
st.markdown("---")

# Chargement modèle
@st.cache_resource
def load_analyzer():
    with st.spinner("Chargement..."):
        return SkinAnalyzer("skin_issues_best.pth")

# Fonction analyse
def analyze_and_display(image_path, image_name):
    try:
        analyzer = load_analyzer()
        
        with st.spinner("Analyse..."):
            result = analyzer.predict(image_path)
            st.session_state.analysis_count += 1
        
        # Résultats
        st.markdown("### 📊 Résultats")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="metric-blue">🔍 {result["skin_issue"]}</div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-blue">📊 {result["confidence"]*100:.1f}%</div>', unsafe_allow_html=True)
        with m3:
            st.markdown('<div class="metric-blue">🤖 MobileNetV3</div>', unsafe_allow_html=True)
        
        # Scores
        st.markdown("#### Scores")
        for classe, score in result['scores'].items():
            st.write(f"**{classe}**")
            st.progress(score, text=f"{score*100:.1f}%")
        
    except Exception as e:
        st.error(f"Erreur: {str(e)}")

# Dossier images test
test_images_dir = "images_test"
test_images = []

if os.path.exists(test_images_dir):
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    for ext in extensions:
        test_images.extend(glob.glob(os.path.join(test_images_dir, ext)))
    test_images = list(set(test_images))
else:
    os.makedirs(test_images_dir)

# Images de test
if test_images:
    st.markdown("### 🖼️ Images test")
    
    cols_per_row = 4
    for i in range(0, len(test_images), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            idx = i + j
            if idx < len(test_images):
                img_path = test_images[idx]
                img_name = os.path.basename(img_path)
                
                with col:
                    img = Image.open(img_path)
                    # ✅ CORRECTION: use_column_width → use_container_width
                    st.image(img, caption=img_name, use_container_width=True)
                    
                    if st.button(f"Analyser", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.selected_image = img_path
                        st.session_state.selected_name = img_name
                        st.rerun()

# Analyse image sélectionnée
if 'selected_image' in st.session_state and st.session_state.selected_image:
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        img = Image.open(st.session_state.selected_image)
        # ✅ CORRECTION: use_column_width → use_container_width
        st.image(img, caption=st.session_state.selected_name, use_container_width=True)
    
    with col2:
        if st.button("Lancer analyse", use_container_width=True):
            analyze_and_display(st.session_state.selected_image, st.session_state.selected_name)
            
            if st.button("Autre image"):
                del st.session_state.selected_image
                del st.session_state.selected_name
                st.rerun()

# Upload utilisateur
st.markdown("---")
st.markdown("### 📤 Ou votre image")

uploaded_file = st.file_uploader(
    "Sélectionner une image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # ✅ CORRECTION: use_column_width → use_container_width
        st.image(image, caption="Votre photo", use_container_width=True)
    
    with col2:
        if st.button("Analyser", use_container_width=True):
            temp_path = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            analyze_and_display(temp_path, "Votre photo")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)

# Footer
st.markdown("---")
st.markdown("⚠️ Outil d'aide - Consultez un professionnel")