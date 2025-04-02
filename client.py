import streamlit as st
import numpy as np
from PIL import Image
import requests
import time

LOCAL_SERVER = 'http://localhost:8000'

def analyseImage(imgNP):
    cnnModelPath = f"{LOCAL_SERVER}/cnn/"
    imageInput = {
        "imageList": imgNP.tolist()
    }
    with st.spinner('Analysing Diseases...'):
        try:
            result = requests.post(cnnModelPath, json=imageInput)
            st.success("Done!")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            return
    if result.status_code == 200:
        disease = result.text
        st.write(f"Disease Detected: {disease}")
        st.markdown("<br /> <br />", unsafe_allow_html=True)
        getSymptoms(disease)
    else:
        st.error("An Error Occurred! Try Again!")


def generate_text_slowly(text, speed=0.1):
    text_placeholder = st.empty()
    chunks = text.split()
    value = ""
    for chunk in chunks:
        value += " " + chunk
        text_placeholder.write(value)
        time.sleep(speed)


def getSymptoms(diseaseClassified):
    llmModelPath = f"{LOCAL_SERVER}/llm/"
    diseaseClass = {
        "disease": diseaseClassified
    }
    with st.spinner(f'Suggesting Help for {diseaseClassified}'):
        try:
            res = requests.post(llmModelPath, json=diseaseClass)
            st.success("Done!")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
            return
    if res.status_code == 200:
        resJSON = res.json()
        st.markdown("<br /> <br /> <br />", unsafe_allow_html=True)
        generate_text_slowly(resJSON['result'])
    else:
        st.error("An Error Occurred! Try Again!")


def main():
    st.title("Skin Diseases Analysis Application")
    with st.form(key='image_form'):
        image = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
        submit_button = st.form_submit_button(label='Analyse')

    if image is not None:
        image_pil = Image.open(image)
        st.image(image_pil, caption='Your uploaded Image', use_container_width=True)
        imageNP = np.array(image_pil, dtype=np.uint8)
        analyseImage(imageNP)


if __name__ == "__main__":
    main()
