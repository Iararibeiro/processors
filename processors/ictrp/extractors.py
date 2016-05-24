# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import base


# Module API

def extract_source(record):
    source = {
        'id': 'ictrp',
        'name': 'WHO ICTRP',
        'type': 'register',
    }
    return source


def extract_trial(record):

    # Get identifiers
    identifiers = {}
    if record['register'] == 'ClinicalTrials.gov':
        identifiers['nct'] = record['main_id']
    if record['register'] == 'EUCTR':
        identifiers['euctr'] = record['main_id']
    if record['register'] == 'ISRCTN':
        identifiers['isrctn'] = record['main_id']

    # Get public title
    public_title = base.helpers.get_optimal_title(
        record['public_title'],
        record['scientific_title'],
        record['main_id'])

    # Get recruitment status
    # (keys are striped and lower-cased)
    statuses = {
        'active, not recruiting': 'pending',
        'approved for marketing': 'other',
        'authorised-recruitment may be ongoing or finished': 'other',
        'available': 'recruiting',
        'closed: follow-up complete': 'other',
        'closed: follow-up continuing': 'other',
        'closed to recruitment: follow up complete': 'other',
        'closed to recruitment: follow up continuing': 'other',
        'complete': 'complete',
        'completed': 'complete',
        'completed: recruitment & data analysis complete': 'complete',
        'complete: follow-up complete': 'complete',
        'complete: follow-up continuing': 'complete',
        'data analysis completed': 'other',
        'enrolling by invitation': 'recruiting',
        'main results already published': 'other',
        'no longer available': 'other',
        'no longer recruiting': 'other',
        'not recruiting': 'other',
        'not yet recruiting': 'pending',
        'open public recruiting': 'recruiting',
        'open to recruitment: actively recruiting participa': 'recruiting',
        '': 'other',
        'other': 'other',
        'pending (not yet recruiting)': 'pending',
        'pending': 'pending',
        'recruiting': 'recruiting',
        'recruitment completed': 'complete',
        'suspended': 'suspended',
        'temporarily closed': 'suspended',
        'temporarily not available': 'suspended',
        'temporary halt or suspension': 'suspended',
        'temporary halt': 'suspended',
        'terminated': 'other',
        'withdrawn': 'other',
        'withheld': 'other',
    }
    recruitment_status = statuses[
        record['recruitment_status'].strip().lower()]

    # Get gender
    gender = None

    # Get has_published_results
    has_published_results = None

    trial = {
        'primary_register': 'WHO ICTRP',
        'primary_id': record['main_id'],
        'identifiers': identifiers,
        'registration_date': None,  # TODO: text on scrap layer
        'public_title': public_title,
        'brief_summary': '',  # TODO: review
        'scientific_title': record['scientific_title'],  # TODO: review
        'description': None,  # TODO: review
        'recruitment_status': recruitment_status,
        'eligibility_criteria': {'criteria': record['key_inclusion_exclusion_criteria']},
        'target_sample_size': record['target_sample_size'],
        'first_enrollment_date': None,  # TODO: text on scraper layer
        'study_type': record['study_type'],
        'study_design': record['study_design'],
        'study_phase': record['study_phase'] or 'N/A',
        'primary_outcomes': record['primary_outcomes'],
        'secondary_outcomes': record['secondary_outcomes'],
        'gender': gender,
        'has_published_results': has_published_results,
    }
    return trial


def extract_conditions(record):
    conditions = []
    for element in record['health_conditions_or_problems_studied'] or []:
        conditions.append({
            'name': element,
            'type': None,
            'description': None,
            'icdcm_code': None,
        })
    return conditions


def extract_interventions(record):
    interventions = []
    for element in record['interventions'] or []:
        # TODO: parse "drug: name"
        interventions.append({
            'name': element,
            'type': None,
            'description': None,
            'icdpcs_code': None,
            'ndc_code': None,
        })
    return interventions


def extract_locations(record):
    locations = []
    for element in record['countries_of_recruitment'] or []:
        locations.append({
            'name': element,
            'type': 'country',
            # ---
            'trial_role': 'recruitment_countries',
        })
    return locations


def extract_organisations(record):
    # TODO: check on scraper level
    organisations = []
    return organisations


def extract_persons(record):
    # TODO: check on scraper level
    persons = []
    return persons
