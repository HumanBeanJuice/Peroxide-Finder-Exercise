# Peroxide-Finder-Exercise

# Prerequisites:
- Docker Installation

# Installation:
- Clone the repository from GitHub
- To run: In the directory of the repository run `docker-compose up --build -d` to build the docker image and start the container detached
- To close: Run `docker-compose down`

# Testing:
- The docker container will remain running until closed.
- To run the test suite:
  -   While the container is running, run the following `docker exec peroxidizer python -m unittest discover`

# Q&A:
- Which of the provided formulated products meet the definition Organic Peroxide under
CFR 173.128(a)(4)? 
`Product 1, Product 2, and Product 3`
- Which of the provided formulated products do not meet the definition?
`Product 4`
- Which subsection under CFR 173.128(a)(4) was used to determine whether the product
meets or does not meet the definition of an Organic Peroxide?
`Product 1, Product 2, and Product 3 are defined as Organic Peroxides under 49 CFR 173.128(a)`
`Product 4 is NOT defined as an Organic Peroxide under 49 CFR 173.128(a)(4)(i)`
- Are any of the products eligible for an exemption?
`Product 4 is exempt under 49 CFR 173.128(a)(4)(i)`


# Commit History and Notes:

Prior to comitting, I used PubChem to add SMILES and molecular weight data to the Product_List.csv file

### a316f74 init: setup app and test files added smiles and mw
Accidental early init

### 5e06898 init: setup files, add smiles and mw to .csv
49 CFR 173.128(a)(4) defines organic peroxide by structure. We can use SMILES to search

### 61e374c Read in .csv with pandas and rename columns
Shorten column names in the dataframe so they are easier to work with and we can use dot notation accessing

### 5e1f4dc Setup classes to represent products and analytes
Using dataclasses to speed up __init__ and __repr__ definitions; slots can also be used.

### 63562fb Add func to get all analytes of product from data
Using the name given to the product instance, can pull in matching data from table (as long as product name exists in table)

### fe7aea2 Add organic perox calc instance method to Product
First check if the Product has already been declared as an ROOR
Then check if any of paragraphs 1-3 are applicable and set to false if so
If not, get a list of all of the peroxide analytes of the product
Finally, if H2O2 is present in the Product, run the formula defined in 49 CFR 173.128(a)(4)(ii)
If the available oxygen exceeds the regulatory limit, set is_organic_peroxide to false and determine which reg applies

### e8b2dbf refactor getanalytes func as instance method
Function makes more sense as an instance method

### 126399c Add post_init to call getanalytes and OrPerox calc
Since we only need the name of the product, we can immediately run both the get_analytes and organic_peroxide_calculator as soon the object is created

### 3ebbb04 Add test for Product object creation
### 32aa98d Add test for is_explosive to test calc func
### a5f4945 Add test for forbidden_for_transport
### 8cdd828 Add test for is_associate_adminster exemption
### c19acc6 Add Product test using .csv where OrP is true
### 2c9abf7 Add tests for 4-1 and 4-2; need test prod in .csv
### afcae0b Add test prod to csv to satisfy 4-2 conditions
Since (hopefully) none of the products were exempt by the 49 CFR 173.128(a)(4)(ii) definition, added a test Product to the .csv that should apply
### 5b34ac0 Add main to init products from csv and print info
### 32a5c31 Freeze dependancies to requirements.txt
### bd572fb Add missing prod_list to outputfunc, cleanup print
### 06171d3 Add dockerfile and docker-compose add to gitignore
### 189ea23 docker-compose.yaml fix keep docker running
The `sh -c tail -F anything` command is a bit hacky, but it keeps the container running while still detached, allowing the ability to run the testing function defined above


