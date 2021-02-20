from NPL_ingester import*
from file_ingester import*
from news_ingester import*
import pytest

def test_NLP():
  assert NLP_analysis("") == "301-file does not exist"

def test_file();
  assert Create("A1",123,"SS") == "100-create successful"
  assert Update("A1",123,"SS") =="110-update successful"
  
def test_new():
  assert new_ingester("")=="201-link not found"
