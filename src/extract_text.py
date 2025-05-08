import pytesseract
from pdf2image import convert_from_path
import PyPDF2
import io
import os
from glob import glob
import streamlit as st
#import wx
from stqdm import stqdm
import sys



def extract_text_from_pdf(pdf_path, output_path):
    pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    
    pdf_writer = PyPDF2.PdfWriter()
    # Loop through each image and extract text using OCR
    for image in images:
        
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
        pdf = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        pdf_writer.add_page(pdf.pages[0])
    
    with open(output_path, "wb") as f:
        pdf_writer.write(f)

def search_pdf_keywords(pdf_path, keywords):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    keyword_dictionary = {}
    keyword_list = []
    file_name = os.path.basename(pdf_path)
    
    for keyword in keywords:
        if keyword.lower() in text.lower():
            keyword_list.append(keyword)
            
        else:
            continue
    if len(keyword_list) > 0:
        keyword_dictionary[file_name] = keyword_list
    return keyword_dictionary



def generate_searchable_pdf(pdf_original_files, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    for file in stqdm(pdf_original_files):
        file_name = os.path.basename(file)
        output_file = os.path.join(output_path, file_name)
        if not os.path.exists(output_file):
            extract_text_from_pdf(file, output_file)
       

def run_keyword_search(pdf_searchable_files,output_path, keywords):
    all_keywords_dict = {}
    for file in stqdm(pdf_searchable_files):
        file_name = os.path.basename(file)
        
        keyword_dict = search_pdf_keywords(file, keywords)
        if len(keyword_dict) > 0:
            all_keywords_dict.update(keyword_dict)
            yield file_name
            
            
        else:
            continue
            

    # Save the keyword dictionary to a file
    output_file = os.path.join(output_path, "keyword_dictionary_new.txt")
    with open(output_file, "w") as f:
        for file_name, keywords in all_keywords_dict.items():
            f.write(f"{file_name}: {', '.join(keywords)}\n")



keyword_dictionary = {}


if __name__ == "__main__":
    
    # The code above extracts text from PDF files using OCR and searches for specific keywords in the extracted text.
    # It uses the PyPDF2 library to read and write PDF files, and the pytesseract library to perform OCR on images.
    # The code also uses the pdf2image library to convert PDF pages to images for OCR processing.
    # The extracted text is saved in a new PDF file, and the keyword search results are saved in a text file.
    # The code is designed to process multiple PDF files in a specified directory and can be easily modified to handle different keywords or output formats.
    # The code is structured to be run as a standalone script, with the main function calling the keyword search function.
    st.title("Convert Non-Searchable PDF's to Searchable PDF's and perform Keyword Search")
    st.write("This app allows you to convert PDF files to searchable PDFs and perform keyword searches on them.")


    if st.checkbox("Generate Searchable PDF's"):
        if st.button("Brows for Original Document Folder"):
           # app = wx.App(True)
           # dialog = wx.DirDialog(None, 'Select a folder:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
           # if dialog.ShowModal() == wx.ID_OK:
           #     pdf_folder = dialog.GetPath() # folder_path will contain the path of the folder you have selected as string
            pdf_folder = st.text_input("Enter the folder path containing PDF files:", None, key="pdf_folder")
            st.write("Specified Folder:", pdf_folder)
            pdf_files_for_processing = glob(os.path.join(pdf_folder, '*.pdf'))
            st.write("Files Found:", pdf_files_for_processing)
            st.write("Converting PDF Files..")
            output_path = os.path.join(pdf_folder, "Searchable_PDFs")
            generate_searchable_pdf(pdf_files_for_processing,output_path)
            st.write("Searchable PDF's Generated in :", output_path)
            #app = wx.App(False)
            #dialog.Destroy()

    if st.checkbox("Run Keyword Search"):
        keywords = st.text_input("Enter Keywords (comma separated):", None, key="keywords")
        st.write("Keywords:", keywords)
        if keywords:
            keywords = [keyword.strip() for keyword in keywords.split(",")]
            st.write("Keywords List:", keywords)
            st.write("Select the folder containing PDF files:")
        
            
            #app = wx.App(True)
            #dialog = wx.DirDialog(None, 'Select a folder:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
            #if dialog.ShowModal() == wx.ID_OK:
            #pdf_searchable_folder = dialog.GetPath() # folder_path will contain the path of the folder you have selected as string
            pdf_searchable_folder = st.text_input("Enter the folder path containing searchable PDF files:", None, key="pdf_searchable_folder")
            st.write("Searchable Files Path:", pdf_searchable_folder)
            pdf_searchable_files = glob(os.path.join(pdf_searchable_folder, '*.pdf'))
            st.write("Files Found:", pdf_searchable_files)
            st.write("Running Keyword Identification..")
            output_path = pdf_searchable_folder
            file_name = run_keyword_search(pdf_searchable_files,output_path, keywords)
            st.write("Keywords Identified in :", file_name)
            #app = wx.App(False)
            #dialog.Destroy()
                
    
    
   


    
