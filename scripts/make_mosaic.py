
# coding: utf-8

# In[5]:

import xarray as xr
import glob, os,sys
folder=sys.argv[1]
postfix=sys.argv[2]
os.chdir(folder)
output=None
for file in glob.glob("*_{}".format(postfix)):
    if(output is None):
        output=xr.open_dataset(file)
    else:
        output=output.combine_first(xr.open_dataset(file))
print output


# In[6]:
comp = dict(zlib=True, complevel=4)
encoding = {var: comp for var in output.data_vars}
output.to_netcdf('mosaico_xarr_{}'.format(postfix),encoding=encoding)


# In[ ]:




