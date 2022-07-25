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

    def calculate_organic_peroxide(self) -> bool:
        '''Calculate whether or not the Product is considered an organic peroxide in accordance with 49 CFR 173.128(a)(4)'''

        if self.is_organic_peroxide == True:
            return self.is_organic_peroxide

        elif self.is_explosive or self.is_forbidden_for_transport or self.is_associate_administer_exempt: # If any of these attributes are True, the 

            self.is_organic_peroxide = False

            if self.is_explosive:
                self.regulatory_definition = '49 CFR 173.128(a)(1)'
            if self.is_forbidden_for_transport:
                self.regulatory_definition = '49 CFR 173.128(a)(2)'
            if self.is_associate_administer_exempt:
                self.regulatory_definition = '49 CFR 173.128(a)(3)'

        else:
            
            peroxide_analytes = [analyte for analyte in self.analytes if 'OO' in analyte.smiles] # Get list of peroxide analytes using smiles where 'OO' is present
            
            if len(peroxide_analytes) > 0:
                self.is_organic_peroxide = True # Start off by setting is_organic_peroxide to True if any OO analytes are present in Product, will be False if exceptions apply
                self.regulatory_definition = '49 CFR 173.128(a)'

            oa_list = []
            oa_max = 0

            if any(peroxide.cas_rn == '7722-84-1' for peroxide in peroxide_analytes): # if hydrogen peroxide cas is present in Product, paragraph 4(i) or 4(ii) of regs may apply
                for analyte in peroxide_analytes:
                    if analyte.max_concentration <= 1.0:
                        oa_max = 1.0 # Sets max allowable available oxygen in accordance with paragraph (4)(i)
                    elif analyte.max_concentration > 1.0 and analyte.max_concentration <= 7.0:
                        oa_max = 0.5

                    n = analyte.smiles.count('OO') # Count number of OO bivalent bonds in analyte SMILES str
                    c = analyte.max_concentration # Assume use of max concentration in accordance with requirements
                    m = analyte.molecular_weight

                    oa_list.append((n*c)/m)

            if oa_list:

                available_oxygen = 16 * sum(oa_list) # Available oxygen formula from 49 CFR 173.128

                if available_oxygen > oa_max: 
                    self.is_organic_peroxide = True
                else:
                    self.is_organic_peroxide = False

                    # Can determine which regulation applies from oa_max
                    if oa_max == 1.0: 
                        self.regulatory_definition = '49 CFR 173.128(a)(4)(i)'
                    elif oa_max == 0.5:
                        self.regulatory_definition = '49 CFR 173.128(a)(4)(ii)'

        return self.is_organic_peroxide


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