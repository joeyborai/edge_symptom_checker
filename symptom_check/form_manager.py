import os
from datetime import date

import pandas as pd
from pandas import ExcelWriter

fields = ['Name', 'Have you traveled outside of the Country in the last 14 days?', 'Have you traveled outside of the tristate (PA, NJ, NY) in the last 14 days?', 'Have you come in contact with anyone diagnosed with or suspected of being infected with COIVD-19 within the last 14 days?', 'Are you experiencing any coughing, shortness of breath, or trouble breathing?', 'Are you experiencing a loss of taste and/or smell?', 'Are you experiencing any fevers, headaches, muscle pain, chills, or repeated shaking with chills?', 'Temperature Reading', 'SignatureVerification']

def _insert_arguments_into_df(arguments):
    df_dict = {
        'Name': [arguments['athlete']],
        'Have you traveled outside of the Country in the last 14 days?': [arguments['countryRadios']],
        'Have you traveled outside of the tristate (PA, NJ, NY) in the last 14 days?': [arguments['tristateRadios']],
        'Have you come in contact with anyone diagnosed with or suspected of being infected with COIVD-19 within the last 14 days?': [arguments['contactRadios']],
        'Are you experiencing any coughing, shortness of breath, or trouble breathing?': [arguments['symptomsRadios']],
        'Are you experiencing a loss of taste and/or smell?': [arguments['tasteRadios']],
        'Are you experiencing any fevers, headaches, muscle pain, chills, or repeated shaking with chills?': [arguments['headacheRadios']],
        'Temperature Reading': [arguments['temperature']],
        'SignatureVerification': ['Yes']
    }

    return df_dict

def create_report(arguments):
    df_dict = _insert_arguments_into_df(arguments)
    df = pd.DataFrame(df_dict)

    day = str(date.today()) if 'day' not in arguments else arguments['day']
    writer = ExcelWriter('/var/www/html/edge_check_in/symptom_check/edge_records/' + str(arguments['athlete']) + day + '.xlsx')
    df.to_excel(writer, 'Sheet1' ,index=False)
    writer.save()

def concatenate_reports():
    day = str(date.today())
    files = os.listdir('/var/www/html/edge_check_in/symptom_check/edge_records/')
    files = [entry for entry in files if day in entry and 'daily' not in entry]

    concatenated_dict = dict()

    for item in files:
        df = pd.read_excel('/var/www/html/edge_check_in/symptom_check/edge_records/' + str(item))

        for field in fields:
            if field in concatenated_dict.keys():
                concatenated_dict[field].append(df[field][0])
            else:
                concatenated_dict[field] = [df[field][0]]

    df = pd.DataFrame(concatenated_dict)

    writer = ExcelWriter('/var/www/html/edge_check_in/symptom_check/edge_records/daily_record' + day + '.xlsx')
    df.to_excel(writer, 'Sheet1' ,index=False)
    writer.save()

    return True

if __name__ == '__main__':
    concatenate_reports()
