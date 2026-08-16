'''
hipdf supports using AMD GPUs for accelerating dataframe operations.
The APIs are similar to those of pandas

For NVIDIA GPUs, you can use cudf in a similar way.

Just need to change one line of code

########################################

0. Installation

1. Example Code

2. Check supported APIs
'''

#-----------------------------------------------------------------------------------------------#
#------------------------------------- 0. Installation -----------------------------------------#
#-----------------------------------------------------------------------------------------------#
'''
For AMD GPUs, check out this link:
https://rocm.docs.amd.com/projects/hipDF/en/latest/install/INSTALL.html

pip3 install amd-hipdf==2.0.0 --extra-index-url=https://pypi.amd.com/rocm-7.0.2/simple
pip3 install -U requests aiohttp

###########################

For NVIDIA GPUs, check out this link:
https://docs.rapids.ai/install/

For cuda 12: 
pip3 install "cudf-cu12==25.12.*"

For cuda 13:
pip3 install "cudf-cu13==25.12.*"
'''

import hipdf
print(hipdf.__version__)
# 2.0.00

import cudf
print(cudf.__version__)
# 25.12.00


#-----------------------------------------------------------------------------------------------#
#------------------------------------- 1. Example Code -----------------------------------------#
#-----------------------------------------------------------------------------------------------#

import os
os.environ["CUDF_PANDAS_BYPASS_XNACK_CHECK"]="1"  # For some AMD GPUs, may need this line to avoid XNACK error

import hipdf as hpd # Change only this line to use hipdf instead of pandas

url = "https://raw.githubusercontent.com/notpeter/crunchbase-data/master/investments.csv"

df_investments = hpd.read_csv(url)

print(df_investments.head())
#                   company_permalink        company_name  ...   funded_at raised_amount_usd
# 0             /organization/0-6-com             0-6.com  ...  2008-03-19         2000000.0
# 1    /organization/004-technologies    004 Technologies  ...  2014-07-24               NaN
# 2  /organization/01games-technology  01Games Technology  ...  2014-07-01           41250.0
# 3              /organization/0xdata              H2O.ai  ...  2015-11-09        20000000.0
# 4              /organization/0xdata              H2O.ai  ...  2013-05-22         3000000.0

'''#########################################################################'''

import cudf as cpd # Change only this line to use cudf instead of pandas

url = "https://raw.githubusercontent.com/notpeter/crunchbase-data/master/investments.csv"

df_investments = cpd.read_csv(url)

print(df_investments.head())
#                   company_permalink        company_name  ...   funded_at raised_amount_usd
# 0             /organization/0-6-com             0-6.com  ...  2008-03-19         2000000.0
# 1    /organization/004-technologies    004 Technologies  ...  2014-07-24               NaN
# 2  /organization/01games-technology  01Games Technology  ...  2014-07-01           41250.0
# 3              /organization/0xdata              H2O.ai  ...  2015-11-09        20000000.0
# 4              /organization/0xdata              H2O.ai  ...  2013-05-22         3000000.0


#-------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Check supported APIs -----------------------------------------#
#-------------------------------------------------------------------------------------------------------#
'''
For hipdf:
https://rocm.docs.amd.com/projects/hipDF/en/latest/reference/hipdf/index.html

######################

For cudf:
https://docs.rapids.ai/api/cudf/stable/user_guide/api_docs/
'''