from __future__ import annotations
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

# Add SMILES and MW data from PubChem to data .csv file

# Read in the .csv file using Pandas
df = pd.read_csv('Product_List.csv', engine='python')

# Rename columns to make them easier to work with
df.rename(columns=
    {
        'Product ID':'product_id',
        'CAS':'cas',
        'SMILES':'smiles',
        'Chemical Name':'name', 
        'Molecular Weight':'mw', 
        'min (%)':'min_conc',
        'max (%)':'max_conc'
    }, inplace=True)
