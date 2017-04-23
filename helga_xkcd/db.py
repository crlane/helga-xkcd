import random

import pymongo
import smokesignal

from helga.db import db
from helga import log

from helga_xkcd.client import XKCDClient

logger = log.getLogger(__name__)


def init_db():
    # setup indexes for text search
    db.xkcd.create_index([('$**', pymongo.TEXT)], background=True)
    db.xkcd.create_index([('num', pymongo.DESCENDING)], background=True, unique=True)


def populate_db(xkcd_client, start, end):
    if end == start:
        end = start + 1
    for i in xrange(start, end + 1):
        try:
            comic = xkcd_client.fetch_number(i)
            db.xkcd.insert_one(comic)
        except Exception as e:
            logger.error(e)
            logger.exception('Error inserting comic %d into database', i)


@smokesignal.on('started')
def populate_database():
    if db is None:  # pragma: no cover
        logger.warning('Cannot ensure xkcd database is up to date. No database connection')
        return
    xkcd_client = XKCDClient()
    max_comic_stored = fetch_latest_comic()
    max_comic_on_site = xkcd_client.fetch_latest()
    if max_comic_stored is None:
        init_db()
        start = 1
        max_num = max_comic_on_site['num']
    else:
        start = max_comic_stored['num'] + 1
        max_num = max_comic_on_site['num']

    if start != max_num:
        populate_db(xkcd_client, start, max_num)


def fetch_latest_comic():
    return db.xkcd.find_one(sort=[('num', pymongo.DESCENDING)])


def fetch_comic_number(number):
    return db.xkcd.find_one({'num': number})


def fetch_random_comic():
    latest = newest()
    if latest is not None:
        return db.xkcd.find_one({'num': random.randint(1, latest + 1)})
    return None


def newest():
    newest = db.xkcd.find_one(sort=[('num', pymongo.DESCENDING)])
    if newest:
        return newest['num']
    return None


def oldest():
    first = db.xkcd.find_one(sort=[('num', pymongo.ASCENDING)])
    if first:
        return first['num']
    return None


def fetch_comic_about(text):
    return db.xkcd.find_one({'$text': {'$search': text}}, {'score': {'$meta': 'textScore'}}, sort=[('score', {'$meta': 'textScore'})])
