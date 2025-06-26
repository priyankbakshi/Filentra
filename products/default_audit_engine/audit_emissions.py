# /products/default_audit_engine/audit_emissions.py

import json
import pandas as pd
import os

# Load EU default values from local JSON file

def load_default_lookup(json_path=None):
    if json_path is None:
        json_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../data/eu_cbam_default_values.json")
        )
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Default values file not found: {json_path}")
    with open(json_path, 'r') as f:
        return json.load(f)

def audit_emissions(df: pd.DataFrame, default_lookup: dict) -> pd.DataFrame:
    flags = {
        'flag_default_cap': [],
        'flag_default_copy': [],
        'flag_outlier_emissions': [],
        'flag_severity': []
    }

    for _, row in df.iterrows():
        cn = str(row['cn_code'])
        direct = row.get('direct_emissions')
        indirect = row.get('indirect_emissions')
        fallback_pct = row.get('default_usage_percentage', 0)

        default_vals = default_lookup.get(cn, {})
        direct_default = default_vals.get('direct')
        indirect_default = default_vals.get('indirect')

        # Rule 1: Fallback cap
        flag_cap = fallback_pct > 20

        # Rule 2: Copy-paste detection (patched)
        flag_copy = (
            fallback_pct > 0 and (
                (abs(direct - direct_default) < 0.001 if direct_default is not None and direct is not None else False) or
                (abs(indirect - indirect_default) < 0.001 if indirect_default is not None and indirect is not None else False)
            )
        )

        # Rule 3: Outlier detection
        flag_outlier = (
            (direct_default and direct is not None and (direct >= 2 * direct_default or direct <= 0.5 * direct_default)) or
            (indirect_default and indirect is not None and (indirect >= 2 * indirect_default or indirect <= 0.5 * indirect_default))
        )

        # Aggregate severity
        if flag_cap or (flag_copy and fallback_pct > 20) or flag_outlier:
            severity = 'Red'
        elif flag_copy or flag_outlier:
            severity = 'Yellow'
        else:
            severity = 'Green'

        flags['flag_default_cap'].append('❌' if flag_cap else '✅')
        flags['flag_default_copy'].append('❌' if flag_copy else '✅')
        flags['flag_outlier_emissions'].append('❌' if flag_outlier else '✅')
        flags['flag_severity'].append(severity)

    for key in flags:
        df[key] = flags[key]

    return df

# For CLI/local testing
if __name__ == "__main__":
    # Example usage
    test_df = pd.DataFrame([
        {
            'cn_code': '25070080',
            'direct_emissions': 0.23,
            'indirect_emissions': 0.08,
            'default_usage_percentage': 22.0
        },
        {
            'cn_code': '25232100',
            'direct_emissions': 2.4,
            'indirect_emissions': 0.10,
            'default_usage_percentage': 15.0
        }
    ])

    defaults = load_default_lookup()
    audited = audit_emissions(test_df, defaults)
    print(audited)
