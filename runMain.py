from pullData import getDates
from matplotlib import pyplot as plt
import numpy as np
from netCDF4 import Dataset

year, month, date, monthConversion = getDates()

def generate_weekly_profs(year,month,date,monthConversion):
	# Opening netCDF4 files
	NC_airTsurf = Dataset("datasets/air.sig995." + str(year) + ".nc", "r", format="NETCDF4")
	NC_uwndSurf = Dataset("datasets/uwnd.sig995." + str(year) + ".nc", "r", format="NETCDF4")
	NC_vwndSurf = Dataset("datasets/vwnd.sig995." + str(year) + ".nc", "r", format="NETCDF4")
	NC_airT = Dataset("datasets/air." + str(year) + ".nc", "r", format="NETCDF4")
	NC_uwnd = Dataset("datasets/uwnd." + str(year) + ".nc", "r", format="NETCDF4")
	NC_vwnd = Dataset("datasets/vwnd." + str(year) + ".nc", "r", format="NETCDF4")
	# Defining for quantity variable
	airTsurf = np.array(NC_airTsurf.variables['air'])
	uwndSurf = np.array(NC_uwndSurf.variables['uwnd'])
	vwndSurf = np.array(NC_vwndSurf.variables['vwnd'])
	airT = np.array(NC_airT.variables['air'])
	uwnd = np.array(NC_uwnd.variables['uwnd'])
	vwnd = np.array(NC_vwnd.variables['vwnd'])
	# Requirements for 250 + 850 mbar extraction
	yearLen = len(airT)
	airT, uwnd, vwnd = airT.reshape(yearLen*17, 73, 144), uwnd.reshape(yearLen*17, 73, 144), vwnd.reshape(yearLen*17,73,144)
	iteratorSkeleton = np.linspace(0,6205,366)
	iterator850 = [int(i+2) for i in iteratorSkeleton]
	iterator250 = [int(i+8) for i in iteratorSkeleton]
	# 250 + 850 mbar extraction
	airT_850mbar = np.array([airT[i] for i in iterator850])
	airT_250mbar = np.array([airT[i] for i in iterator250])
	uwnd_850mbar = np.array([uwnd[i] for i in iterator850])
	uwnd_250mbar = np.array([uwnd[i] for i in iterator250])
	vwnd_850mbar = np.array([vwnd[i] for i in iterator850])
	vwnd_250mbar = np.array([vwnd[i] for i in iterator250])
	# Index prep for 365-day year array call + leap year correction
	if len(airTsurf) == 366:
		leapYear = True
	newDate = 0
	for elem in monthConversion.keys():
		if elem != month:
			newDate += (monthConversion[elem])[1]
		else:
			newDate += date
			break
	if leapYear == True and newDate > 59:
		newDate += 1
	# Extracting week-long margin for 9 arrs (redefining)
	airTsurf = airTsurf[newDate-3:newDate+4]
	airT_250mbar = airT_250mbar[newDate-3:newDate+4]
	airT_850mbar = airT_850mbar[newDate-3:newDate+4]
	uwndSurf = uwndSurf[newDate-3:newDate+4]
	uwnd_250mbar = uwnd_250mbar[newDate-3:newDate+4]
	uwnd_850mbar = uwnd_850mbar[newDate-3:newDate+4]
	vwndSurf = vwnd[newDate-3:newDate+4]
	vwnd_250mbar = vwnd_250mbar[newDate-3:newDate+4]
	vwnd_850mbar = vwnd_850mbar[newDate-3:newDate+4]
	outData = np.array([airTsurf, airT_250mbar, airT_850mbar, uwndSurf,
	 uwnd_250mbar, uwnd_850mbar, vwndSurf, vwnd_250mbar, vwnd_850mbar])
	np.save("outData/9qty-7day-2dSpatial_profiles_9x7x73x144_.npy",outData)
	return 0

# npy example centered on November 7 2020.