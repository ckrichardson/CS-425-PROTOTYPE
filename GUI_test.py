import pytest
from binaryAnalysis.GUI import *
import atlastk
from binaryAnalysis.find_network_sigs import *
from unittest.mock import patch

def pytest_report_header(config):
    """ 
    Pytest Header
    """
    return "binaryAnalysis/GUI"

def test_generateIDAttrBody():
    """
    Testing if the correct HTML is returned when not __main__
    """
    body = generateIDAttrBody()
    assert "Enter email" in body

def test_integrity_btn_status_one():
    """
    Testing return status when all 3 integrity radio buttons are false
    """
    assert integrity_btn_status("false", "false", "false") == False

def test_integrity_btn_status_two():
    """
    Testing return status when 3rd radio button is true
    """
    assert integrity_btn_status("false", "false", "true") == True

def test_integrity_btn_status_three():
    """
    Testing return status when 2nd radio button is true
    """
    assert integrity_btn_status("false", "true", "false") == True

def test_integrity_tban_status_four():
    """
    Testing return status when 1st radio button is true
    """
    assert integrity_btn_status("true", "false", "false") == True

def test_graphics_btn_status_one():
    """
    Testing when both graphics radio buttons are false
    """
    assert graphics_btn_status("false", "false") == False

def test_graphics_btn_status_two():
    """
    Testing when 2nd radio button is true
    """
    assert graphics_btn_status("false", "true") == True

def test_graphics_btn_status_three():
    """
    Testing when 1st radio button is true
    """
    assert graphics_btn_status("true", "false") == True

@patch('os.path.isfile')
def test_path_one(mock_file_path_good):
    """
    Testing good file path with mock
    """
    def return_values(path):
        if path == "/root/CS-425-PROTOTYPE/binaryAnalysis/100.PRG":
            return True
        else:
            return False

    mock_file_path_good.side_effect = return_values
    assert file_path_good("/root/CS-425-PROTOTYPE/binaryAnalysis/100.PRG") == True
    assert file_path_good("/rot/CS-425-PROTOTYPE/binaryAnalysis/100.PRG") == False

def test_acConnect():
    """
    Testing acConnect
    """ 
    assert acConnect("blah") == False

def test_acEndAnalysis():
    """
    Testing acEndAnalysis
    """
    assert acEndAnalysis("blah") == None
