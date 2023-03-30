####################################################
## services.py
## 03.30.2023 - Jonathan Moore - RGS
####################################################
import data


###############################################
## GET_ACCOUNT_LIST
## Return tuple of string months (Januaury,....)
################################################
def get_account_list() -> tuple:
    return tuple(data.query_distinct_account_name())