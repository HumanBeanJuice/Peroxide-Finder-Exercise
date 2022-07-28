from __future__ import annotations
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
import re

# Add SMILES and MW data from PubChem to data .csv file

# Read in the .csv file using Pandas
df = pd.read_csv('Product_List.csv', engine='python')

# Definte anticipaated inorganic analytes
inorganic_analytes = ['15630-89-4', '497-19-8']

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
    is_organic: bool=True

    def __post_init__(self) -> None:
        if self.cas_rn in inorganic_analytes:
            self.is_organic = False

@dataclass
class Product():
    '''Product that contains a collection of Analyte(s) (constituents)'''

    name: str
    is_organic_peroxide: bool = False # Default attributes to False
    regulatory_definition: str = ''
    is_explosive: bool = False
    is_forbidden_for_transport: bool = False
    is_associate_administer_exempt: bool = False 
    analytes: list(Analyte) = field(init=False, default_factory=list)

    def get_product_analytes(self, product_name) -> list(Analyte):
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
            
            # In the future, could also use flat formula (or calculate implicit hydrogens from SMILES) to find C-H bonds to identify inorganic analytes
            organic_peroxide_analytes = [analyte for analyte in self.analytes if 'OO' in analyte.smiles and analyte.is_organic == True] # Get list of peroxide analytes using smiles where 'OO' is present and the analyte is considered organic
            

            if len(organic_peroxide_analytes) > 0:
                self.is_organic_peroxide = True # Start off by setting is_organic_peroxide to True if any OO analytes are present in Product, will be False if exceptions apply
                self.regulatory_definition = '49 CFR 173.128(a)'

            elif len(organic_peroxide_analytes) <= 0:
                self.is_organic_peroxide = False # Unless there are no organic_peroxides
                self.regulatory_definition = '49 CFR 173.138(a) - Inorganic or No bivalent -O-O- containing compounds'

            oa_list = []
            oa_max = 0

            if any(peroxide.cas_rn == '7722-84-1' for peroxide in organic_peroxide_analytes): # if hydrogen peroxide cas is present in Product, paragraph 4(i) or 4(ii) of regs may apply
                for analyte in organic_peroxide_analytes:
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

    # Once a new Product has been initialized with a name, we have all the info we need to get its analytes and run the calculate_organic_peroxide func
    def __post_init__(self) -> None:
        try:
            self.analytes = self.get_product_analytes(self.name)
            self.calculate_organic_peroxide()
        except KeyError as e:
            print(e)
            self.analytes = []



def main() -> None:

    product1 = Product(
        name='Product 1'
    )

    product2 = Product(
        name='Product 2'
    )

    product3 = Product(
        name='Product 3'
    )

    product4 = Product(
        name='Product 4'
    )

    product_list = [product1, product2, product3, product4]

    def output(prod_list: list[Product]) -> None:

        print(f'{[(analyte.name, analyte.is_organic) for analyte in product3.analytes]=}')
        print('\nProducts defined as an Organic Peroxide under CFR 173.128(a)(4):')
        for product in product_list:
            if product.is_organic_peroxide == True:
                print('Product: ',product.name, ', Regulatory Definition: ', product.regulatory_definition)

        print('\nProducts NOT defined as an Organic Peroxide under CFR 173.128(a)(4):')
        for product in product_list:
            if product.is_organic_peroxide == False:
                print('Product: ',product.name, ', Regulatory Definition: ', product.regulatory_definition)

    output(product_list)

if __name__ == '__main__':
    main()
