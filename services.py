import os

####################################################
## services.py
## 03.30.2023 - Jonathan Moore - RGS
####################################################
import data


#####################################################
#####################################################    
def get_db_file():
    return os.path.join(os.getcwd(), "bills.db")