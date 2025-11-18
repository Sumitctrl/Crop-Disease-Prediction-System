# 🌿 Crop Disease Prediction System

✨ **Live App:** (https://crop-disease-prediction-system.streamlit.app/)

A Streamlit web application that uses a deep learning model...
A Streamlit web application that uses a deep learning model (TensorFlow/Keras) to identify common diseases in crop leaves from user-uploaded images. This system is designed to provide quick, accessible diagnostic support to farmers and agricultural enthusiasts.

#✨ Features
Image Upload: Easily upload an image of a crop leaf for analysis.

Instant Prediction: Uses a trained Convolutional Neural Network (CNN) model to predict the specific disease or determine if the leaf is healthy.

High Accuracy: Built on a robust dataset for reliable disease classification.

Web Interface: Hosted on Streamlit Cloud for easy access and use.

#💻 Installation and Setup
This project can be run locally or is automatically deployed on Streamlit Cloud.

Prerequisites
You need Python 3.10 (or a compatible version, see notes below) and pip installed.

Local Setup
Clone the Repository:

Bash

git clone https://github.com/Sumitctrl/Crop-Disease-Prediction-System.git
cd Crop-Disease-Prediction-System
Create a Virtual Environment:

Bash

python3.10 -m venv myenv
source myenv/bin/activate  On Linux/macOS
Or: .\myenv\Scripts\activate  On Windows (Command Prompt/PowerShell)
Install Dependencies: Use the environment.yml or requirements.txt file to install all necessary packages. Since the project uses TensorFlow and Streamlit, it's best to use the environment.yml for stability.

Bash

 If using environment.yml (Recommended)
conda env create -f environment.yml
conda activate crop-disease-prediction 
(Note: If you don't use Conda, use the provided requirements.txt with a compatible Python 3.10 environment.)

Run the App
Start the Streamlit application using the main Python file:

Bash

streamlit run app1.py
The application will open in your default web browser (usually at http://localhost:8501).
