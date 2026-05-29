# 🔬 SkinAnalyzer

A Streamlit application for skin issue analysis using a fine-tuned MobileNetV3 deep learning model.

## Features

- Upload and analyze skin images
-  Deep learning-based classification
- Confidence scores for each prediction
- Supports JPG, JPEG, and PNG formats

## Installation

```bash
git clone https://github.com/salmaMlika/SkinAnalyzer.git
cd SkinAnalyzer
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Project Structure

```plaintext
SkinAnalyzer/
├── app.py                 # Streamlit application
├── skin_analyzer.py       # Model loading and prediction logic
├── skin_issues_best.pth   # Trained MobileNetV3 model
├── requirements.txt       # Project dependencies
├── images_test/           # Sample test images
└── README.md
```

## Model

The application uses a fine-tuned MobileNetV3 model trained to classify common skin conditions:

- Acne
- Blackheads
- Dark Spots
- Enlarged Pores
- Wrinkles

## Requirements

- Python 3.8+
- Streamlit
- PyTorch
- Torchvision
- Pillow

## Disclaimer

⚠️ This project is intended for educational and informational purposes only. It is **not a medical diagnostic tool** and should not replace professional medical advice.

## License

MIT License
