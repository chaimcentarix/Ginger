import json

METADATA_FILENAME_PATH = "/home/ester/Downloads/metadata_epi_v6_189k.jsonl"  # TODO move here: "data/metadata.nd_json"
metadata = {json.loads(l).get('_id',0):json.loads(l) for l in open(METADATA_FILENAME_PATH).readlines()}


def extract_gsm(s):
    # To extract the GSM from the user's input
    l = s.find('GSM')
    if l > -1:
        # That means there is GSM there
        gsm = 'GSM'
        for u in range(min(len(s) - (l + 3), 20)):
            t = s[l + 3 + u]
            if t.isnumeric():
                gsm += t
        return gsm
    return None