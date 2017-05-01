import mock
import pytest

from functools import partial
from helga_xkcd import command


MOCK_CLIENT = 'irc'
MOCK_CHANNEL = 'bots'
MOCK_NICK = 'crlane'
MOCK_MESSAGE = 'foobar'
MOCK_CMD = '!xkcd'


MOCK_ARGS = [
    MOCK_CLIENT,
    MOCK_CHANNEL,
    MOCK_NICK,
    MOCK_MESSAGE,
    MOCK_CMD
]


@pytest.fixture
def mock_helga_command():
    '''A partial helga command hook'''
    return partial(command.xkcd, *MOCK_ARGS)


@pytest.fixture
def mock_subcommand():
    return mock.Mock()


@pytest.mark.parametrize('args,expected_subcommand', [
    ((), 'latest_comic_command'),
    (('latest',), 'latest_comic_command'),
    (('random',), 'random_comic_command'),
    (('refresh',), 'refresh_db_command'),
    (('refresh', 10), 'refresh_db_command'),
    (('about', 10), 'comic_about_command'),
    (('number', 10), 'comic_number_command'),
], ids=['empty', 'latest', 'random', 'refresh-empty', 'refresh-args', 'about-args', 'number-args'])
def test_command_calls_correct_subcommand(args, expected_subcommand, monkeypatch, mock_subcommand, mock_helga_command):
    monkeypatch.setattr(command, expected_subcommand, mock_subcommand)
    mock_helga_command(args)
    assert mock_subcommand.call_count == 1
