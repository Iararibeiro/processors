# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'gsk',
        'name': 'GlaxoSmithKline',
        'type': 'register',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = base.helpers.clean_dict({
        'nct': record['clinicaltrialsgov_identifier'],
        'gsk': record['study_id'],
    })

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['study_title'],
        record['official_study_title'],
        record['study_id'])

    # Get recruitment status
    statuses = {
        'Active, not recruiting': 'other',
        'Active not recruiting': 'other',
        'Completed': 'complete',
        'Not yet recruiting': 'pending',
        'Recruiting': 'recruiting',
        'Suspended': 'suspended',
        'Terminated': 'other',
        'Withdrawn': 'other',
    }
    recruitment_status = statuses[record['study_recruitment_status']]

    # Get gender
    gender = None
    if record['gender']:
        gender = record['gender'].lower()

    # Get has_published_results
    has_published_results = False
    if record['protocol_id']:
        has_published_results = True

    trial = {
        'primary_register': 'GlaxoSmithKline',
        'primary_id': record['study_id'],
        'identifiers': identifiers,
        'registration_date': record['first_received'],
        'public_title': public_title,
        'brief_summary': record['brief_summary'] or '',  # TODO: review
        'scientific_title': record['official_study_title'],  # TODO: review
        'description': record['detailed_description'],
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {
            'criteria': record['eligibility_criteria'],  # TODO: bad text - fix on scraper
        },
        'target_sample_size': record['enrollment'],  # TODO: review
        'first_enrollment_date': record['study_start_date'],
        'study_type': record['study_type'] or 'N/A',  # TODO: review
        'study_design': record['study_design'] or 'N/A',  # TODO: review
        'study_phase': record['phase'] or 'N/A',  # TODO: review
        'primary_outcomes': record['primary_outcomes'] or [],
        'secondary_outcomes': record['secondary_outcomes'] or [],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    for element in record['conditions'] or []:
        conditions.append({
            'name': element,
            'type': None,
            'description': None,
            'icdcm_code': None,
        })
    return conditions


def extract_interventions(record):
    # TODO: record['interventions'] - reimplement on scraper - array -> dict
    interventions = []
    return interventions


def extract_locations(record):
    # TODO: no recruitment countries field
    locations = []
    return locations


def extract_organisations(record):
    # TODO: discover how to get it/fix it on scraper
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: discover how to get it/fix it on scraper
    persons = []
    return persons
