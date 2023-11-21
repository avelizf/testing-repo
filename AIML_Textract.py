import streamlit as st
import boto3, datetime, time

st.set_page_config(page_title="Toolbox", page_icon="🛠️")
st.title('Textract demo')

#######################
###      Setup      ###
#######################
s3 = boto3.client('s3')
textract = boto3.client('textract')
bucket_name = 'textract-demo-20231103001'   # Setup your bucket name
input_folder = 'input/'
out_doc_folder = 'output_doc/'
out_exp_folder = 'output_exp/'

#########################
###      ToolBox      ###
#########################
# define  upload_to_s3 function to upload files selected in uploaded_files=st.file_uploader to s3 bucket using boto3
def upload_to_s3(uploaded_files):
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        s3.put_object(Bucket=bucket_name, Key=input_folder+uploaded_file.name, Body=bytes_data)
    return 


#########################
### Streamlit content ###
#########################

with st.form("selector_form"):

    uploaded_files = st.file_uploader("Choose an image file", accept_multiple_files=True, type=["png", "jpg", "jpeg"], help="Upload only png, jpg, jpeg files")
    submitted = st.form_submit_button(label='Submit', help='Submit files to s3 bucket', on_click=upload_to_s3(uploaded_files), args=None)

    progress_text = "Operation in progress. Please wait..."
    my_bar = st.progress(0, text=progress_text)
    # Step 02: Check files in s3 bucket
    st.write('''
        **Loaded files in S3 bucket:**
    ''')
    progress=0
    resp_json_all = {}
    for uploaded_file in uploaded_files:
        st.write(f''' - {uploaded_file.name}
        ''')
        # check if uploaded_file.name starts with "document" or not
        if uploaded_file.name.startswith("document"):
            # if it starts with "document", then call textract to extract text from the document
            # get document text from textract
            resp_doc_analysis = textract.start_document_analysis(
                DocumentLocation = {
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': input_folder+uploaded_file.name
                    }
                },
                FeatureTypes=[
                    'TABLES',
                ],
                OutputConfig={
                    'S3Bucket': bucket_name,
                    'S3Prefix': out_doc_folder+datetime.datetime.now().strftime("%Y-%m-%d")
                }
            )
            progress+=25
            my_bar.progress(progress, text=f'Analysing {uploaded_file.name}...')
            # wait 5 sec to get success status
            time.sleep(10)
            response = textract.get_document_analysis(
                JobId=resp_doc_analysis['JobId'],
            )
            progress+=25
            my_bar.progress(progress, text=f'Analysing {uploaded_file.name}...')
        elif uploaded_file.name.startswith("expense"):
            resp_expense_analysis = textract.start_expense_analysis(
                DocumentLocation = {
                    'S3Object': {
                        'Bucket': bucket_name,
                        'Name': input_folder+uploaded_file.name
                    }
                },
                OutputConfig={
                    'S3Bucket': bucket_name,
                    'S3Prefix': out_exp_folder+datetime.datetime.now().strftime("%Y-%m-%d")
                }
            )
            progress+=25
            my_bar.progress(progress, text=f'Analysing {uploaded_file.name}...')
            # wait 5 sec to get success status
            time.sleep(10)
            response = textract.get_expense_analysis(
                JobId=resp_expense_analysis['JobId'],
            )
            progress+=25
            my_bar.progress(progress, text=f'Analysing {uploaded_file.name}...')
        else:
            response = ''
        # add to resp_json_all dict all json responses
        resp_json_all[uploaded_file.name] = response
        
    # Step 03: Textract files uploaded in batch
    if len(resp_json_all) == len(uploaded_files) and len(resp_json_all) != 0:
        st.write('''
            #### JSON data:
        ''')
        st.json(resp_json_all, expanded=True)

        st.balloons() # celebrate!



