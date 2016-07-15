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
    name = helpers.clean_string(extract_CanonicalName(location['name']))
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
def extract_CanonicalName(location):
    try:
        canonical_name = countries.get(location).name
        logger.debug('Location - %s: %s','normalized', canonical_name)
    except KeyError:
        canonical_name = location
        # This part is for looking for matching cases (suggestion), uses the 
        # fuzzy logic to get the country name who get 80% of match rate.
        with open(os.path.join(os.path.dirname(__file__),'countries.csv'), 'r') as f:
            countries_data = csv.reader(f, delimiter= str(u','))
            logger.debug('Location - %s: %s','not normalized', canonical_name)

            for country in countries_data:
                unicode_row = [x.decode('utf8') for x in country]
                if (fuzz.ratio(location, unicode_row) > 80):
                    canonical_name = countries.get(country[1]).name
                    logger.debug('Location - %s: %s','not normalized with the most close result', canonical_name)

        

    return canonical_name