import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import re
import time
from uuid import uuid4
import logging
import requests
import config
import json

def get_sentiment(cont):
    
    data = dict()
    data['content'] = cont
    header_conf = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(config.sentiment_api, data=json.dumps(data), headers=header_conf)
    return response.json()

def save_file(req):
    
    logging.debug("Save file request is received......")
    file = req.files['file']
    id = uuid4()
    file_path_name = os.getcwd()+'/files/'+ str(id) + "_"+file.filename
    logging.debug("Current file is {}".format(file_path_name))
    try:
        logging.debug("Saving path to {}".format(file_path_name))
        resp = file.save(file_path_name)
    except Exception as exp:
        logging.error("Failed to save file,{}".format(str(exp)))
    print(resp)
    return file_path_name, file.filename
    
def extract_text_from_pdf(filepath):
    
    output_string = StringIO()
    with open(filepath, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    logging.debug("File is processed, Deleting temporay file")
    try:
        
        print("test")
    except Exception as exp:
        logging.info("Faile to delete temporary file")
    return output_string.getvalue()
