import os
import time
import openai
import logging
from datetime import datetime
import slack
import gpt
#logging.basicConfig(filename='mylog.log', level=#logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
current_time = time.time()
print("Server started...")

def get_timestamp():
        return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

while True:
    # In order to answer the applicant's last question, we turn to the Slack server in each iteration and request the message history and extract the last message from there
    # We check if the message is not a response of this code and also if it is new to know that it is new we save the beginning of the running time of the code and if we enter a new message from the beginning of the running of the code we save the time of the new message
    time.sleep(0.5)

    #logging.info(f"{get_timestamp()}: Waiting...")

    try:
            if slack.get_slack_message(current_time):
                question, message_time, gsm_metadata=slack.get_slack_message(current_time)
                current_time = message_time
                response = ''
                if gsm_metadata !='0':
                    response = gpt.build_a_response(
                        f'Please take this data: {gsm_metadata} example and formulate an answer to the following question: {question}')
                else:
                    response = gpt.build_a_response(question)

                # timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                #logging.info(f"Operation at {timestamp}: question='{question}', response='{response}'")

                result = slack.post_slack(response=response)
                gpt.make_sumarry()
                # timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                #logging.info(f"Operation at {timestamp}: question='{question}', response='{response}', result='{result}'")
    except Exception as e:
            timestamp = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            logging.error(f"Error at {timestamp}: {e}")
            print(f"Error at {timestamp}: {e}")



# TODO: add this to test {'_index': 'gene_ontology_epic', '_type': 'metadata', '_id': 'GSM1412246', '_score': None, '_source': {'sample_name': 'GSM1412246', 'title': 'Differential methylation in CN-AML preferentially targets non-CGI regions and is dictated by DNMT3A mutational status and associated with predominant hypomethylation of HOX genes.', 'status': 'Public on Jul 31 2014', 'submission_date': 'Jun 13 2014', 'last_update_date': 'Jul 31 2014', 'type': 'genomic', 'channel_count': '1', 'organism_ch1': 'Homo sapiens', 'taxid_ch1': '9606', 'molecule_ch1': 'genomic DNA', 'extract_protocol_ch1': 'DNA and RNA was extracted by TRIzol ( Invitrogen) or ALLPrep ( QIAGEN ) according to the standard instructions. Sample quanlity were tested by Genomic DNA ScreenTape.', 'label_ch1': 'Cy5 and Cy35', 'label_protocol_ch1': 'Standard Illumina Protocol', 'hyb_protocol': 'bisulphite converted DNA was amplified,