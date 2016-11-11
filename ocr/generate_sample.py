import os
from utils import process_sample_cards, write_sample_result
from predictions import make_predictions

if __name__ == '__main__':
    print ('Starting - Generate Sample data file.')

    base_path = '/home/jitendra/poc/cards'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/jitendra/poc/ocr/cred.json'

    sample_ocr_data = process_sample_cards(base_path=base_path)
    cards_predicted_data = {}
    for dir_name, ocr_data in sample_ocr_data.iteritems():
        cards_predicted_data[dir_name] = make_predictions(ocr_data)

    result_file_path = write_sample_result(cards_predicted_data=cards_predicted_data)

    print ('Sample result stored at: %s' % result_file_path)