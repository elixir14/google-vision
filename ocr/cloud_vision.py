#!/usr/bin/env python
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This script uses the Vision API's OCR capabilities to find and index any text
a set of images. It builds an inverted index, and uses redis
(http://redis.io/) to persist the index. By default, the script asumes a local
redis install set up to persist to disk. Assuming the redis database is
persisted between runs, the script can be run multiple times on the same set
of files without redoing previous work. The script uses also nltk
(http://www.nltk.org/index.html) to do stemming and tokenizing.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt

Then, follow the instructions here:
http://www.nltk.org/data.html to download the necessary nltk data.

Run the script on a directory of images to create the index, E.g.:

    ./textindex.py <path-to-image-directory>

Then, instantiate an instance of the Index() object (via a script or the
Python interpreter) and use it to look up words via the Index.lookup() or
Index.print_lookup() methods.  E.g.:

    import textindex
    index = textindex.Index()
    index.print_lookup('cats', 'dogs')

This will return all the images that include both 'cats' and 'dogs' in
recognizable text. More exactly, it will return all images that include text
with the same stems.
"""

import argparse
# [START detect_text]
import base64
import os
import re
import sys

GOOGLE_APPLICATION_CREDENTIALS= "cred.json"

from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials



DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
BATCH_SIZE = 10


class VisionApi:
    """Construct and use the Google Vision API service."""

    def __init__(self, api_discovery_file='vision_api.json'):
        self.credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_text(self, input_filenames, num_retries=3, max_results=16):
        """Uses the Vision API to detect text in the given file.
        """
        images = {}
        for filename in input_filenames:
            with open(filename, 'rb') as image_file:
                images[filename] = image_file.read()

        batch_request = []
        for filename in images:
            batch_request.append({
                'image': {
                    'content': base64.b64encode(
                            images[filename]).decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }]
            })
        request = self.service.images().annotate(
            body={'requests': batch_request})

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return {}
            text_response = {}
            for filename, response in zip(images, responses['responses']):
                if 'error' in response:
                    print("API Error for %s: %s" % (
                            filename,
                            response['error']['message']
                            if 'message' in response['error']
                            else ''))
                    continue
                if 'textAnnotations' in response:
                    text_response[filename] = response['textAnnotations']
                else:
                    text_response[filename] = []
            return text_response
        except errors.HttpError as e:
            print("Http Error for %s: %s" % (filename, e))
        except KeyError as e2:
            print("Key error: %s" % e2)
# [END detect_text]
