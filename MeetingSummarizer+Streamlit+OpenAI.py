#--- Open AI Meeting Summarizer APP with stream lit --- 

#importing required libraries 

import openai
import streamlit as st 
import os
from docx import Document
from azure.identity import DefaultAzureCredential

''' After importing required libraries, authentication with OPEN AI APIs is required'''

#setting the keys 
AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE") or "oai-oaibot-poc-buzz"
AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHATGPT_DEPLOYMENT") or "gpt-35-turbo"

os.environ['AZURE_CLIENT_ID']='#add your Azure Client ID'
os.environ['AZURE_CLIENT_SECRET']='#add your Azure Client ID Secret'
os.environ['AZURE_TENANT_ID']='#add your Azure Tenant ID'
azure_credential = DefaultAzureCredential()

''' After setting up authentication, connect to Azure OpenAI services and pass the keys'''

# Used by the OpenAI SDK
openai.api_type = "azure"
openai.api_base = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com"
openai.api_version = "2023-03-15-preview"

openai.api_type = "azure_ad"
openai.api_key = azure_credential.get_token("https://cognitiveservices.azure.com/.default").token

''' -- Designing the Streamlit UI --'''

#designing the steamlit UI
st.set_page_config(layout="wide")
st.markdown(r""" # MEETING NOTES SUMMARIZER :memo:""")

st.markdown(f"""<style>.stApp {{
             background-image: url("#Add your background-attachment"
             background-attachment: fixed;
             background-size: cover}}</style>""",unsafe_allow_html=True)

st.subheader("Powered by AI")
st.text("This app allows you to create minutes of meeting instantly! Upload a file and see the magic...")
st.markdown("---")
#widget to create file upload option
uploaded_file = st.file_uploader("Upload transcript file", accept_multiple_files=False,type=['docx'] )

def read_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
         full_text.append(para.text)
    return '\n'.join(full_text)

#create Radio buttons
output_size = st.radio(label="What type of summary you require?",
                       options=["To-the-point", "Concise", "Detailed"]
                       )

if output_size == "To-the-point":
     out_token = 50
elif output_size == "Concise":
     out_token = 128
else:
     out_token = 516

""" Writing Meeting organizer logic """

#adding app conditions
if uploaded_file is not None:
    doc_text = read_docx(uploaded_file)
    if st.button("Generate Meeting Summary"):
        st.write("AI is generating an answer, please wait....")
        #use GPT-3 to generate a summary of the text 
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = "Please summarize this meeting conversation in meeting notes format with bullet points : " 
            + doc_text,
            max_tokens = out_token,
            temperature = 0.5)

        #print the summary generated 
        res = response['choices'][0]["text"]
        st.info(res)

        st.download_button("Download Summary",res)
else:
    st.warning("It seems you haven't uploaded a file.Please upload a valid transcript file(.docx)")