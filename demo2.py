import numpy as np
import streamlit as st
from skimage.io import imread
from skimage.transform import resize
import pickle
import webbrowser as wb
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load models
model1 = pickle.load(open('Models/KCRaa.pkl', 'rb'))  # LogisticRegression
model2 = pickle.load(open('Models/KCRkaa.pkl', 'rb'))
model3 = pickle.load(open('Models/KCRnum.pkl', 'rb'))

# Define character lists
characters_list_1 = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ', 'ಎ', 'ಏ', 'ಐ', 'ಒ', 'ಓ', 'ಔ', 'ಅಂ', 'ಅಃ']
characters_list_2 = {'17': 'ಕ್', '18': 'ಕ', '19': 'ಕಾ', '20': 'ಕಿ',
                     '21': 'ಕೀ', '22': 'ಕು', '23': 'ಕೂ', '24': 'ಕೃ', '25': 'ಕೈ', '26': 'ಕೆ', '27': 'ಕೇ', '28': 'ಕೈ',
                     '29': 'ಕೊ', '30': 'ಕೋ', '31': 'ಕೌ', '32': 'ಕಂ', '33': 'ಕಃ'}
characters_list_3 = {'648': '೦', '649': '೧', '650': '೨',
                     '651': '೩', '652': '೪', '653': '೫', '654': '೬', '655': '೭', '656': '೮', '657': '೯'}


def transform_image(img):
    # Resize and flatten the image
    transform_img = resize(img, (150, 150, 3))
    flatten_img = transform_img.flatten()
    return flatten_img


# --------------UI Beginning------------
# SideBar
side_bar = st.sidebar.radio(
    'Select Characters', ['Characters(ಅ-ಅಃ)', 'Characters(ಕ-ಕಃ)', 'Characters(೦-೯)', 'About'])


# Helper function to display metrics
def display_metrics(model_file, img_dir):
    o = Get_Model(img_dir, model_file)
    accuracy, f1, recall, precision, conf_matrix = o.build_model()
    st.write(f'Accuracy: {accuracy}')
    st.write(f'F1 Score: {f1}')
    st.write(f'Recall: {recall}')
    st.write(f'Precision: {precision}')
    st.write('Confusion Matrix:')
    st.write(conf_matrix)
    st.image(f'Models/{model_file}_conf_matrix.png')


# Page 1: Characters(ಅ-ಅಃ)
if side_bar == 'Characters(ಅ-ಅಃ)':
    st.title('Kannada Character Recognition (ಅ-ಅಃ)')
    st.header('Pick a Test Image')
    img_name = st.file_uploader('Select Image')
    if img_name is not None:
        try:
            img = imread(img_name)
            st.image(img)
            img_transformed = transform_image(img)
        except:
            st.error('Failed to load image.')

        # Predict Button
        if st.button('Predict Character'):
            try:
                res1 = model1.predict([img_transformed])  # Predict using model1
                st.header(f'Predicted Character is {characters_list_1[res1[0] - 1]}')
            except:
                st.error('Failed to predict character.')

        # Display Metrics Button
        if st.button('Display Metrics'):
            display_metrics('KCRaa', 'test_img_aa/')


# Page 2: Characters(ಕ-ಕಃ)
elif side_bar == 'Characters(ಕ-ಕಃ)':
    st.title('Kannada Character Recognition (ಕ-ಕಃ)')
    st.header('Pick a Image (from test_img_ka)')
    img_name = st.file_uploader('Select Image')
    if img_name is not None:
        try:
            img = imread(img_name)
            st.image(img)
            img_transformed = transform_image(img)
        except:
            st.error('Failed to load image.')

        # Predict Button
        if st.button('Predict Character'):
            try:
                res2 = model2.predict([img_transformed])  # Predict using model2
                res2 = str(res2[0])
                st.header(f'Character is {characters_list_2[res2]}')
            except:
                st.error('Failed to predict character.')

        # Display Metrics Button
        if st.button('Display Metrics'):
            display_metrics('KCRkaa', 'test_img_ka/')


# Page 3: Characters(೦-೯)
elif side_bar == 'Characters(೦-೯)':
    st.title('Kannada Character Recognition (೦-೯)')
    st.header('Pick a Image (from test_img_num)')
    img_name = st.file_uploader('Select Image')
    if img_name is not None:
        try:
            img = imread(img_name)
            st.image(img)
            img_transformed = transform_image(img)
        except:
            st.error('Failed to load image.')

        # Predict Button
        if st.button('Predict Character'):
            try:
                res3 = model3.predict([img_transformed])  # Predict using model3
                res3 = str(res3[0])
                st.header(f'Predicted Character is {characters_list_3[res3]}')
            except:
                st.error('Failed to predict character.')


# About
elif side_bar == 'About':
    st.title('About Project')
    st.text('''
        -Kannada OCR (Optical Character Recognition) with ML (Machine Learning)
        classification algorithm involves training a machine learning model to recognize
        and classify Kannada characters from scanned or digital images.
        -OCR technology has become increasingly important in recent years due to the growth of
        digitization and the need to process large volumes of documents quickly and
        accurately.OCR technology is used in a variety of applications, including data
        entry, document archiving, and information retrieval.
        -Kannada OCR with ML classification algorithm is especially important for preserving and digitizing
        Kannada literature and documents.Kannada is a Dravidian language spoken
        predominantly in the Indian state of Karnataka.Kannada literature is rich and
        diverse, with a history that spans over a thousand years.However, much of this
        literature remains in print form and is not easily accessible to the wider
        public.
        -OCR technology can help to digitize these documents, making them more
        easily accessible to scholars and researchers.
        -ML classification algorithms are used to classify Kannada characters based on their visual features. These
        algorithms learn from a set of training data, and then use this knowledge to
        classify new data. Some popular ML classification algorithms for OCR include
        Support Vector Machines (SVM), Random Forests, and Convolutional Neural
        Networks (CNN), Logistic Regression. 
        -We have implemented Logistic Regression. 
        ''')

    if st.button('Report Bug'):
        wb.open("https://gmail.google.com/mail/?view=cm&fs=1&to=gowthamigs2002@gmail.com.com&su=Bug%20Report")
