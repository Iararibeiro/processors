# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
import logging
import datetime

from iso3166 import countries
from fuzzywuzzy import fuzz
import os
import csv

from .. import readers
from .. import helpers
logger = logging.getLogger(__name__)


# Module API

def write_location(conn, location, source_id, trial_id=None):
    """Write location to database.

    Args:
        conn (dict): connection dict
        location (dict): normalized data
        source_id (str): data source id
        trial_id (str): related trial id

    Raises:
        KeyError: if data structure is not valid

    Returns:
        str/None: object identifier/if not written (skipped)

    """
    create = False
    timestamp = datetime.datetime.utcnow()

    # Get name
    name = normalize_location(helpers.clean_string(location['name']))
    if len(name) <= 1:
        return None

    # Get slug/read object
    slug = helpers.slugify_string(name)
    object = readers.read_objects(conn, 'locations', first=True, slug=slug)

    # Create object
    if not object:
        object = {}
        object['id'] = uuid.uuid4().hex
        object['created_at'] = timestamp
        object['slug'] = slug
        create = True

    # Write object only for high priority source
    if create or source_id:  # for now do it for any source

        # Update object
        object.update({
            'updated_at': timestamp,
            'source_id': source_id,
            # ---
            'name': name,
            'type': location.get('type', None),
        })

        # Write object
        conn['database']['locations'].upsert(object, ['id'], ensure=False)

        # Log debug
        logger.debug('Location - %s: %s',
            'created' if create else 'updated', name)

    return object['id']

#----helper function to get the canonical name of the locations
def normalize_location(location):
    base_similarity = 0
    country_alpha = 3
    THRESHOLD = 80

    _format_location = lambda x: x.decode('utf8').lower().strip().replace(".", "")
    _max_index_and_value = lambda arr: max(enumerate(arr), key=lambda x: x[1])

    location_name = _format_location(location)
    try:
        location_name = countries.get(location_name).name
        logger.debug('Location - %s: %s normalized using the lib', location, location_name)
    except KeyError:
        with open(os.path.join(os.path.dirname(__file__), 'countries.csv'), 'r') as f:
            countries_data = [tuple(line) for line in csv.reader(f, delimiter=',')]
            similarity_with_countries = [fuzz.ratio(location_name, _format_location(country[base_similarity])) for country in countries_data]
            max_index, max_value = _max_index_and_value(similarity_with_countries)
            if max_value >= THRESHOLD:
                location_name = countries.get(countries_data[max_index][country_alpha]).name
                logger.debug('Location - %s: %s normalized using country name similarity', location, location_name)
            else:
                base_similarity = 21
                similarity_with_capitals = [fuzz.ratio(location_name, _format_location(country[base_similarity])) for country in countries_data]
                max_index, max_value = _max_index_and_value(similarity_with_capitals)
                if max_value >= THRESHOLD:
                    location_name = countries.get(countries_data[max_index][country_alpha]).name
                    logger.debug('Location - %s: %s normalized using capital name similarity', location, location_name)
                else:
                    logger.debug('Location - %s: %s not normalized', location, location_name)
    return location_name