import pygrib
# demonstrates basic functionality of module
# open a grib file, create an iterator.
grbs = pygrib.open('sampledata/flux.grb')
# iterate over all grib messages.
print '-- all %d messages --' % grbs.messages
for grb in grbs:
    print grb
# position iterator at beginning again.
grbs.rewind() 
print '-- all messages (again)  --'
for grb in grbs:
    print grb
# get a specific grib message from the iterator.
# iterator will be positioned at this message.
grb = grbs.message(2) 
print '-- 2nd message --'
print grb # 2nd message
# position iterator at next grib message.
grb = grbs.next() 
print '-- 3rd message --'
print grb # 3rd message
# now the iterator should be positioned at the last (4th) message.
print '-- iterate from 4th message to the end--'
for grb in grbs:
    print grb # only last message printed.
# rewind again
grbs.rewind()
print '-- Maximium temperature --'
# iterate over all messages until
# 'Maximum temperature' is found.
for grb in grbs:
    if grb['name'] == 'Maximum temperature': break
print grb
# get the data and the lat/lon values of the Max temp grid 
data = grb['values'] # 'values' returns the data
print '-- data values, grid info for msg number %d --' % \
grb.messagenumber # current message number
print 'shape/min/max data',data.shape,data.min(), data.max()
lats, lons = grb.latlons() # returns lat/lon values on grid.
print 'min/max of %d lats on %s grid' % (grb['Nj'], grb['typeOfGrid']),\
lats.min(),lats.max()
print 'min/max of %d lons on %s grid' % (grb['Ni'], grb['typeOfGrid']),\
lons.min(),lons.max()

# get first grib message
grb = grbs.message(1)
# turn bitmap on.
grb['bitmapPresent']=1
# get the data.
data = grb['values']
# put a hole of missing values in the data.
nx = grb['Ni']; ny = grb['Nj']
data[ny/4:ny/2,nx/4:nx/2]=grb['missingValue']
grb['values']=data
# open an output file for writing
grbout = open('test.grb','w')
# get coded binary string for modified message
msg = grb.get_message()
# write to file and close.
grbout.write(msg)
grbout.close()

# reopen file and plot
grbs = pygrib.open('test.grb')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
grb = grbs.message(1)
lats, lons = grb.latlons()
data = grb['values']
llcrnrlon = lons[0,0]
llcrnrlat = lats[0,0]
urcrnrlon = lons[-1,-1]
urcrnrlat = lats[-1,-1]
m = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat,
            resolution='c',projection='cyl')
x,y = m(lons,lats)
m.drawcoastlines()
m.contourf(x,y,data,15)
plt.title('Modifed Grib Data')
plt.show()
