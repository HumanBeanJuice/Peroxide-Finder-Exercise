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

# Setup classes that represent a Product and Analyte Objects

@dataclass
class Analyte():
    '''Represents a chemical/compound'''

    name: str
    cas_rn: str
    smiles: str
    min_concentration: float
    max_concentration: float
    molecular_weight: float

@dataclass
class Product():
    '''Product that contains a collection of Analyte(s) (constituents)'''

    name: str
    analytes: list[Analyte]
    is_organic_peroxide: bool = False # Default attributes to False
    regulatory_definition: str = ''
    is_explosive: bool = False
    is_forbidden_for_transport: bool = False
    is_associate_administer_exempt: bool = False 


def get_product_analytes(product_name) -> list(Analyte):
    '''Retrieves all of the analytes of a given product, used in Product class post_init'''
    return [
        Analyte(
            name=row.name,
            cas_rn=row.cas,
            smiles=row.smiles,
            molecular_weight=row.mw,
            min_concentration=row.min_conc,
            max_concentration=row.max_conc
        ) for row in df[df['product_id'] == product_name].itertuples()
    ]