# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import requests
import datetime
from .. import base
logger = logging.getLogger(__name__)


# Module API

def process(conf, conn):

    # Tables to export
    TABLES = [
        'locations',
    ]

    # Export tables
    # http://jamdb.readthedocs.io/en/latest/index.html
    token_ttl_seconds = 30*60  # api has limit 60*60 seconds
    token_issued_time = datetime.datetime.now()
    session = requests.Session()
    for table in TABLES:

        # Log started
        logger.info('Started "%s" export', table)

        # Ensure authentificated
        if (datetime.datetime.now() - token_issued_time).seconds > token_ttl_seconds:
            del session.headers['Authorization']
        if 'Authorization' not in session.headers:
            url = '%s/auth' % conf['OSF_URL']
            res = session.post(url, json={
              'data': {
                'type': 'users',
                'attributes': {
                  'provider': 'osf',
                  'access_token': conf['OSF_KEY'],
                }
              }
            })
            # Check status
            # 200 - ok
            if res.status_code not in [200]:
                logger.error('Can\'t authentificate', table)
                exit(1)
            token = res.json()['data']['attributes']['token']
            session.headers.update({'Authorization': token})
            logger.info('Succesefully authentificated')

        # Ensure collection exists
        url = '%s/namespaces/%s/collections'
        url = url % (conf['OSF_URL'], conf['OSF_NAMESPACE'])
        res = session.post(url, json={
            'data': {
                'id': table,
                'type': 'collections',
                'attributes': {},
            }
        })
        # Check status
        # 201 - created
        # 409 - conflict
        if res.status_code not in [201, 409]:
            logger.error('Can\'t create "%s" collection', table)
            exit(1)
        logger.info('Ensured collection "%s" exists', table)

        # Export rows
        count = 0
        bufsize = 100
        url = '%s/namespaces/%s/collections/%s/documents'
        url = url % (conf['OSF_URL'], conf['OSF_NAMESPACE'], table)
        for rows in _read_grouped_rows(conn, table, bufsize):
            # We use bulk post
            # https://github.com/CenterForOpenScience/jamdb/blob/master/features/document/create.feature#L244
            data = []
            for row in rows:
                data.append({
                    'id': row['id'],
                    'type': 'documents',
                    'attributes': json.loads(json.dumps(
                        row, cls=base.helpers.JSONEncoder)),
                })
            res = session.post(url, json={'data': data}, headers={
                'Content-Type': 'application/vnd.api+json; ext="bulk"',
            })
            # Check status
            # 201 - created
            # 409 - conflict
            if res.status_code not in [201, 409]:
                logger.error('Can\'t create "%s" documents', table)
                exit(1)
            count += len(data)
            logger.info('Exported %s "%s"' % (count, table))

        # Log finished
        logger.info('Finished "%s" export', table)


# Internal

def _read_grouped_rows(conn, table, bufsize=100):
    """Yields lists of rows with max bufsize length.
    """
    rows = []
    for row in base.readers.read_rows(conn, 'database', table, orderby='id'):
        rows.append(row)
        if len(rows) >= bufsize:
            yield rows
            rows = []
    if rows:
        yield rows
