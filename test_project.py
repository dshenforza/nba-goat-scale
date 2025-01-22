from project import get_goat_table, get_player, concat_tables, table_sorter
import pandas as pd
import pytest_mock
import pytest
import unittest
from unittest.mock import MagicMock, patch
import sys


"""
The first three tests are for the 3 possible outcomes of the get_goat_table function
"""
def test_get_goat_table_valid_input_yes(mocker):
    # Setup all the mock objects - input, NBA API Calls, data frames
    mocker.patch('builtins.input', return_value='y')
    mock_find_players = mocker.patch('project.players.find_players_by_full_name')
    mock_find_players.return_value = [{'id': 123}]

    mock_career_stats = mocker.patch('project.playercareerstats.PlayerCareerStats')
    mock_career_stats.return_value.get_data_frames.return_value = [
        pd.DataFrame(),  # for get_data_frames[0] - not used in function
        pd.DataFrame({   # Mock version of career totals data frame
            'PLAYER_NAME': ['Michael Jordan'],
            'PLAYER_ID': [123],
            'GP': [1072],
            'PTS': [32292],
            'REB': [6672],
            'AST': [5633]
        })
    ]

    # Call the function
    result = get_goat_table()

    # Verify the output
    assert isinstance(result, pd.DataFrame)

def test_get_goat_table_valid_input_no(mocker):
    mocker.patch('builtins.input', return_value ='n')
    with pytest.raises(SystemExit):
        get_goat_table()

def test_get_goat_table_invalid(mocker):
    mocker.patch('builtins.input', return_value='scooby doo')
    with pytest.raises(SystemExit):
        get_goat_table()


def test_get_player_valid_player(mocker):
    mocker.patch('builtins.input', return_value='Valid Player Name')
    mocker.patch('project.players.find_players_by_full_name', return_value=[{'id': 'valid_id'}])
    mock_career_stats = mocker.patch('project.playercareerstats.PlayerCareerStats')
    
    mock_df = pd.DataFrame({
        'PLAYER_NAME': [],
        'PLAYER_ID': [],
        'GP': [],
        'PTS': [],
        'REB': [],
        'AST': []
    })
    
    mock_career_stats.return_value.get_data_frames.return_value = [None, mock_df]

    result = get_player()
    assert isinstance(result, pd.DataFrame)

def test_get_player_no_player_found(mocker):
    mocker.patch('builtins.input', return_value='Invalid Player Name')
    mocker.patch('project.players.find_players_by_full_name', return_value=[])
    with pytest.raises(SystemExit):
        get_player()

def test_table_sorter():
    data = {
        'PLAYER_ID': [1, 2],
        'PTS': [30, 20],
        'REB': [10, 5],
        'AST': [5, 10],
        'GP': [10, 10]
    }
    table = pd.DataFrame(data)

    with patch('builtins.input', return_value='PTS'):
        sorted_table = table_sorter(table)

    expected_data = {
        'PTS': [30, 20],
        'REB': [10, 5],
        'AST': [5, 10],
        'GP': [10, 10],
        'PTS/gm': [3.0, 2.0],
        'REB/gm': [1.0, 0.5],
        'AST/gm': [0.5, 1.0]
    }
    expected_table = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(sorted_table, expected_table)