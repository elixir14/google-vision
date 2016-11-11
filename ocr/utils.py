import os
import uuid
from logging import getLogger
import logging
import itertools


logging.basicConfig()
logger = getLogger(__name__)
from cloud_vision import VisionApi
from constants import UserField

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR_NAME = 'card_result'
def get_ocr_data(images = []):
    vision_api = VisionApi()
    vision_response = vision_api.detect_text(images)
    locale = ''
    response_data = {}
    for file_path, value in vision_response.iteritems():
        if value:
            #data = value[0]['description'].replace('\n', ' ')
            response_data[file_path] =  value[0]['description'].split('\n')

    return response_data



def get_sample_file_list(base_path):
    card_dirs = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
    card_files = {}
    for card_dir in card_dirs:
        card_files[card_dir] = [os.path.join(base_path, card_dir, file_name)
                                for file_name in ['front.jpg', 'back.jpg']]
    return card_files


def get_card_file_list(sample_card_list):

    card_files = []

    for file_path in list(itertools.chain.from_iterable(sample_card_list.values())):
        if os.path.exists(file_path):
            card_files.append(file_path)
            logger.debug('Adding card file (%s) to list.' % file_path)
        else:
            logger.warn('card file (%s) not provided !!!' % file_path)

    return card_files


def process_sample_cards(base_path):
    sample_card_list = get_sample_file_list(base_path)
    card_files = get_card_file_list(sample_card_list)

    ocr_data = get_ocr_data(images=card_files)
    sample_ocr_data = {}
    for item, card_file_list in sample_card_list.iteritems():
        card_dir_data = []
        for card_file_path in card_file_list:
            if card_file_path in ocr_data.keys():
                card_dir_data += ocr_data.get(card_file_path)

        sample_ocr_data[item] = card_dir_data

    return sample_ocr_data


def get_entries(data, max_entries):
    return_data = [''] * max_entries
    counter = 0
    for item in data[:max_entries]:
        return_data[counter] = item
        counter += 1
    return return_data

def write_sample_result(cards_predicted_data):
    result_file_path = os.path.join(BASE_DIR, RESULT_DIR_NAME, str(uuid.uuid4()) + '.csv')
    if not os.path.exists(os.path.dirname(result_file_path)):
        os.makedirs(os.path.dirname(result_file_path), mode=0777)
    header = ["Card Directory", "Email 1", "Email 2", "Email 3",
              "Website 1", "Website 2", "Website 3",
              "Phone 1", "Phone 2", "Phone 3"
              ]
    with open(result_file_path, 'w') as result_file:
        result_file.write("%s\n" % ",".join(header))
        for directory_name, predicted_data in cards_predicted_data.iteritems():
            data = []
            data.append(directory_name)
            data += get_entries(predicted_data['email'], 3)
            data += get_entries(predicted_data['website'], 3)
            data += get_entries(predicted_data['phone_number'], 3)
            if len(header) != len(data):
                logger.error("Data count error!!!! Header count: %d, data count: %d, data: (%s)"
                             % (len(header), len(data), str(data)))
                print("Data count error!!!! Header count: %d, data count: %d, data: (%s)"
                             % (len(header), len(data), str(data)))
                continue

            result_file.write("%s\n" % ",".join(data))
    return result_file_path

# sample_card_list = get_sample_file_list(base_path)
# print sample_card_list.values()
# print list(itertools.chain.from_iterable(sample_card_list.values()))
# card_files = get_card_file_list(sample_card_list)