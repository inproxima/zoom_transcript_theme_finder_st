import streamlit as st
import os
import openai
import docx2txt
import textwrap
from PyPDF2 import PdfFileReader

#page config
st.set_page_config(page_title="Zoom Transcript Analyzer", page_icon="🤖", initial_sidebar_state="expanded")
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""
#st.markdown(hide_st_style, unsafe_allow_html=True)

#functions
def get_summary( prompt, text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.0,
            max_tokens=900,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text

def get_minutes(prompt, output):
        # Use OpenAI's GPT-3 model to generate a summary of the text
        themes = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_minutes,
            max_tokens=2024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return themes.choices[0].text

#Buffer for all files
@st.cache
def docx_to_txt(docx_filename, txt_filename=None):
    text = docx2txt.process(docx_filename)
    # Write the text to the txt file, using utf-8 encoding
    return text

@st.cache
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read() 

@st.cache
def read_pdf(file):
	pdfReader = PdfFileReader(file)
	count = pdfReader.numPages
	all_page_text = ""
	for i in range(count):
		page = pdfReader.getPage(i)
		all_page_text += page.extractText()

	return all_page_text


st.title("Zoom Transcript Analyzer")
st.markdown("""---""") 
st.subheader("Please input your OpenAI API key")
url = "https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key"
api = st.text_input("If you don't know your OpenAI API key click [here](%s)." % url, type="password", placeholder="Your API Key")
#st.write("If you don't know your OpenAI API key click [here](%s" % url)
openai.api_key = api
st.markdown("""---""") 
st.subheader("Please Upload Your Transcipt")
docx_file = st.file_uploader("Upload Document",
    type=["pdf","docx","txt"])
analyzer = st.text_input("What would you like me to look for?", placeholder="i.e., key takeaways")


# Check Openai Key
if st.button("Process File"):
    try:
        # Send a test request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="What is the capital of France?",
            temperature=0.5
    )
        st.markdown("""---""")
        st.success("API key is valid!")
    
    except Exception as e:
        st.error("API key is invalid: {}".format(e))
    
    if docx_file is not None:
        with st.spinner(text="With words that rhyme and numbers bright, this AI shall analyze with all its might..."):
            st.subheader("Analysis Results")
            if docx_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                raw_text = docx_to_txt(docx_file)
                output = ''
                chunks = textwrap.wrap(raw_text, 6500)
                result = ''
                for chunk in chunks:
                    prompt1 = (f"Generate meeting minutes from the following Zoom transcript:\n{chunk}\n")
                    summary_large = get_summary(prompt1, chunk)
                    result = result + ' ' + summary_large
                output = output + result
                prompt_minutes = (f"What are the {analyzer} discussed in the TEXTS: {output}")
                output_minutes = get_minutes(prompt_minutes, output)
                st.write(output_minutes)
            elif docx_file.type == "text/plain":
                raw_text = str(docx_file.read(), "utf-8")
                output = ''
                chunks = textwrap.wrap(raw_text, 6500)
                result = ''
                for chunk in chunks:
                    prompt1 = (f"Generate meeting minutes from the following Zoom transcript:\n{chunk}\n")
                    summary_large = get_summary(prompt1, chunk)
                    result = result + ' ' + summary_large
                output = output + result
                prompt_minutes = (f"What are the {analyzer} discussed in the TEXTS: {output}")
                output_minutes = get_minutes(prompt_minutes, output)
                st.write(output_minutes)
            elif docx_file.type == "application/pdf":
                raw_text = read_pdf(docx_file)
                raw_text = docx_to_txt(docx_file)
                output = ''
                chunks = textwrap.wrap(raw_text, 6500)
                result = ''
                for chunk in chunks:
                    prompt1 = (f"Generate meeting minutes from the following Zoom transcript:\n{chunk}\n")
                    summary_large = get_summary(prompt1, chunk)
                    result = result + ' ' + summary_large
                output = output + result
                prompt_minutes = (f"What are the {analyzer} discussed in the TEXTS: {output}")
                output_minutes = get_minutes(prompt_minutes, output)
                st.write(output_minutes)
                





