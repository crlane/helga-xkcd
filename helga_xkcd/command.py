from helga import log
from helga import settings
from helga.plugins import command

from helga_xkcd import db

logger = log.getLogger(__name__)

EPSILON = 10 ** -3
TEXT_SCORE_THRESHOLD = getattr(settings, 'XKCD_TEXT_SCORE_THRESHOLD', 0.75)


def within_importance_threshold(score):
    """
    checks if the given text seach score is within the configured threshold
    for importance.
    """
    return (score - TEXT_SCORE_THRESHOLD) >= EPSILON


def stringify_post(comic):
    """Prepares the dictionary representation of a comic for posting to the channel

    Note that due to the way helga works, this will result in multiple line response.
    """
    return u'{img}\nTitle: {safe_title} Alt: {alt}'.format(**comic)


def comic_number_command(client, channel, number):
    comic = db.fetch_comic_number(number)
    logger.debug('Comic returned from db: %s', comic)
    if comic:
        return stringify_post(comic)
    else:
        msg = 'No comic by that number. Choose a number between {min} and {max}'
        new = db.newest()
        old = db.oldest()
        if new and old:
            msg = 'No comic by that number. Choose a number between {min} and {max}'
            return msg.format(min=old, max=new)
        else:
            return 'The current index contains {count}'.format(count=db.xkcd.find().count())


def latest_comic_command(client, channel):
    comic = db.fetch_latest_comic()
    if comic:
        logger.debug('Fetched latest comic: %s', comic)
        return stringify_post(comic)


def comic_about_command(client, channel, text):
    comic = db.fetch_comic_about(text)
    if comic:
        if within_importance_threshold(comic.get('score', 0)):
            logger.debug('Fetched comic about %s: %s', text, comic)
            return stringify_post(comic)
        else:
            msg = ('Fetched comic number %d, but the score was below importance threshold (%f < %f).'
                   'If this happens consistently, lower the threshold in settings.')
            logger.debug(msg, comic['num'], comic['score'], TEXT_SCORE_THRESHOLD)

            return 'No comics score high enough to be about {text}. Can you be more specific?'.format(text=text)
    return u"Randall hasn't made a comic about {text}".format(text=text)


def random_comic_command(client, chanel):
    comic = db.fetch_random_comic()
    if comic:
        logger.debug('Fetched random comic: %s', comic)
        return comic['img']


@command('xkcd', help="Show an xkcd comic. Usage: helga xkcd (number <int>|random|about <text> ...)")
def xkcd(client, channel, nick, message, cmd, args):
    """
    Manages listing plugins, or enabling and disabling them
    """
    if len(args) < 1:
        subcmd = 'latest'
    else:
        subcmd = args[0]

    if subcmd == 'latest':
        return latest_comic_command(client, channel)

    if subcmd == 'number':
        try:
            number = int(args[1])
        except ValueError:
            logger.exception("Got bad integer argument for number")
            return 'number subcommand requires integer as second argument'
        return comic_number_command(client, channel, number)

    if subcmd == 'random':
        return random_comic_command(client, channel)

    if subcmd == 'about':
        text = args[1:]
        return comic_about_command(client, channel, ' '.join(text))
