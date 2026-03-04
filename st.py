import streamlit as st
from cli.cow import image_to_ascii
from PIL import Image

st.title('COW')
st.write('Upload an image to convert it to ASCII art.')

uploaded_file = st.file_uploader('Upload an image', type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    ratio = st.slider('Resize ratio divider', min_value=1.0, max_value=3.0, value=2.0, step=0.1)
    width = st.slider('ASCII art width', min_value=16, max_value=512, value=200, step=8)
    invert = st.checkbox('Invert ASCII art')

    if st.button('Convert'):
        ascii_art = image_to_ascii(image, ratio, width, invert)
        st.code(ascii_art, language='ascii_art')