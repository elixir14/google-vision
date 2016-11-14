import re
from logging import getLogger

from django.db.models import Count

from .models import ScannedCardDetail
from constants import UserField
logger = getLogger(__name__)


def make_predictions(input_list):
    """
    The function will process list and return dictionary of prediction tag with matches.
    :param input_list:
    :return prediction_map:
    """
    logger.debug("make_predictions called!!!")
    prediction_map = {'email':[], 'website':[], 'phone_number':[]}

    for line, text in enumerate(input_list):
        email = check_email_address(text)
        if email:
            prediction_map['email'] = prediction_map['email'] + email

        website = check_website(text)
        if website:
            prediction_map['website'] = prediction_map['website'] + website

        phone_number = check_phone_number(text)
        if phone_number:
            prediction_map['phone_number'] = prediction_map['phone_number'] + phone_number

    logger.debug("make_predictions returns %s" % str(prediction_map))
    return prediction_map


def predicate_item(input_text):
    if check_email_address(input_text):
        return UserField.EMAIL_1
    if check_website(input_text):
        return UserField.WEBSITE_1
    if check_phone_number(input_text):
        return UserField.PHONE_1

    return predict_from_existing_records(input_text=input_text)


def predict_from_existing_records(input_text):
    predicated_caption_summary = ScannedCardDetail.objects.values('accepted_caption').annotate(
        num_instances=Count('accepted_caption')).filter(text=input_text)
    print input_text
    print predicated_caption_summary.query
    predicated_caption = UserField.UNKNOWN
    num_instances = 0
    for item in predicated_caption_summary:
        if item['accepted_caption'] != UserField.UNKNOWN:
            if int(item['num_instances']) > num_instances:
                num_instances = int(item['num_instances'])
                predicated_caption = int(item['accepted_caption'])

    return predicated_caption


def check_email_address(input_text):
    """
    Helper function to check if given text contains valid email address.
    :param input_text:
    :return matched email(s) address or None:
    """
    email_address = None
    email_address = re.findall(r'[\w\.-]+@[\w\.-]+', input_text)
    return email_address


def check_website(input_text):
    """

    :param input_text:
    :return:
    """
    GRUBER_URLINTEXT_PAT = re.compile(
        ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')

    matches = GRUBER_URLINTEXT_PAT.findall(input_text)
    websites = []
    if matches:
        for match in matches:
            if match:
                websites.append(match[0])
    return websites


def check_phone_number(input_text):
    """

    :param input_text:
    :return:
    """
    url_pattern = "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    return re.findall(url_pattern, input_text)


# dummy_data = ['why people dont know what regex are? let me know 321dsasdsa@dasdsa.com.lol  '
#               ' dssdadsa dadaads@dsdds.com','jitendra.sanghani@gmail.com is foignsfd f@foo.com',
#               'https://google.com', 'https://www.google.com','CA94305-1234', '650.123.4567']
#make_predictions(input_list=dummy_data)
# check_website('https://google.com')
# check_website('https://www.google.com')
# check_website('www.google.com')
# check_website('www.google.ll')

# check_phone_number('CA94305-1234')
# check_phone_number('650.123.4567')
