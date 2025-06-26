# /products/default_audit_engine/tests/test_audit_emissions.py

import pandas as pd
import sys
import os

# Patch root path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../../"))
sys.path.insert(0, PROJECT_ROOT)

from products.default_audit_engine.audit_emissions import audit_emissions, load_default_lookup

def test_default_cap_breach():
    row = {
        'cn_code': '25070080',
        'direct_emissions': 0.23,
        'indirect_emissions': 0.08,
        'default_usage_percentage': 25.0
    }
    df = pd.DataFrame([row])
    result = audit_emissions(df, load_default_lookup())
    assert result['flag_default_cap'][0] == '❌'
    assert result['flag_severity'][0] == 'Red'

def test_copy_paste_detection():
    row = {
        'cn_code': '25070080',
        'direct_emissions': 0.23,
        'indirect_emissions': 0.07,
        'default_usage_percentage': 10.0
    }
    df = pd.DataFrame([row])
    result = audit_emissions(df, load_default_lookup())
    assert result['flag_default_copy'][0] == '❌'
    assert result['flag_severity'][0] == 'Yellow'

def test_outlier_emissions():
    row = {
        'cn_code': '25070080',
        'direct_emissions': 0.05,  # <0.5× default (0.23)
        'indirect_emissions': 0.08,
        'default_usage_percentage': 5.0
    }
    df = pd.DataFrame([row])
    result = audit_emissions(df, load_default_lookup())
    assert result['flag_outlier_emissions'][0] == '❌'
    assert result['flag_severity'][0] == 'Red'

def test_all_flags_green():
    row = {
        'cn_code': '25070080',
        'direct_emissions': 0.20,
        'indirect_emissions': 0.07,
        'default_usage_percentage': 10.0
    }
    df = pd.DataFrame([row])
    result = audit_emissions(df, load_default_lookup())
    assert result['flag_default_cap'][0] == '✅'
    assert result['flag_default_copy'][0] == '✅'
    assert result['flag_outlier_emissions'][0] == '✅'
    assert result['flag_severity'][0] == 'Green'

def test_red_combo_flags():
    row = {
        'cn_code': '25070080',
        'direct_emissions': 0.23,
        'indirect_emissions': 0.08,
        'default_usage_percentage': 35.0
    }
    df = pd.DataFrame([row])
    result = audit_emissions(df, load_default_lookup())
    assert result['flag_default_cap'][0] == '❌'
    assert result['flag_default_copy'][0] == '❌'
    assert result['flag_severity'][0] == 'Red'

if __name__ == '__main__':
    test_default_cap_breach()
    test_copy_paste_detection()
    test_outlier_emissions()
    test_all_flags_green()
    test_red_combo_flags()
    print("✅ All unit tests passed for audit_emissions")
