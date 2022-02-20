import pandas as pd
import geopandas as geo
from shapely.geometry import Polygon, Point
from shapely.strtree import STRtree
import numpy as np
import time

import matplotlib.pyplot as plt

start_time = time.time()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

AUTmap = geo.read_file("Daten/raster_austria.gpkg", rows=10)

#df = pd.read_csv("Daten/rtr_datensatz_2019_2020_komplett.csv", sep=",", nrows=100)

columns_needed = [
"network_type",
"lat",
"long",
"loc_accuracy",
"country_location",
"download_kbit",
"upload_kbit",
"ping_ms",
"lte_rsrp",
"lte_rsrq",
"platform",
"model",
"network_name",
"ndt_download_kbit",
"ndt_upload_kbit",
"implausible",
"signal_strength",
"pinned",
"dtm_level",
"signal_classification"]

df = pd.read_csv("Daten/rtr_datensatz_2019_2020_komplett.csv", nrows=1000, sep=",", usecols = columns_needed)

#Daten geeignet filtern.
df = df.drop(df[(df.country_location != "AT") | (df.implausible != False) | (df.loc_accuracy > 150)].index)
#  gelöschte Spalten ['loc_accuracy', 'country_location', 'implausible']
df = df.drop(labels=['loc_accuracy', 'country_location', 'implausible'], axis=1)


gdf = geo.GeoDataFrame(
    df, geometry=geo.points_from_xy(df.long,df.lat),crs="EPSG:4326")
gdf = gdf.to_crs("EPSG:31287")
gdf = gdf.drop(labels=['lat', 'long'], axis=1)


################################ALGO############

Points = gdf.geometry
tree = STRtree(Points)

AUTmap = AUTmap.assign(AverageDOWNLOAD = 0)
AUTmap = AUTmap.assign(AverageUPLOAD = 0)
AUTmap['IndexListe'] = np.empty((len(AUTmap), 0)).tolist()

start_time = time.time()

i = 0
for p in AUTmap.geometry:

    #res = [x for x in tree.query(p) if p.contains(x)]
    res = tree.query(p)
    if len(res) >= 1:
             var = gdf[gdf.isin(res).any(axis=1)]
             #print(var)
             #print(sum(var['download_kbit'])/len(var['download_kbit']))
             #AUTmap.loc[i,'AverageDOWNLOAD'] = sum(var['download_kbit'])/len(var['download_kbit'])
             #AUTmap.loc[i, 'AverageUPLOAD'] = sum(var['upload_kbit'])/len(var['upload_kbit'])
             AUTmap.loc[i, 'IndexListe'].append(var.index.tolist())
             #print(AUTmap.loc[i, 'IndexListe'])

    i = i+1
###############################################

print(time.time()-start_time)

#AUTmap.to_csv("AUTmapAVERAGES_Test.csv")
AUTmap_FILTER = AUTmap.drop(AUTmap[(AUTmap.AverageDOWNLOAD == 0)].index)
#AUTmap_FILTER.to_csv("AUTmap_Filer_AVERAGES_Test.csv")
print(len(AUTmap_FILTER))
print(AUTmap.head(50))
#
# Filtered_points = pd.read_csv("AUTmapAVERAGES.csv", sep=",")
# Filtered_points = Filtered_points.drop(Filtered_points[(Filtered_points.AverageDOWNLOAD == 0)].index)
# Filtered_points.to_csv("Filtered_points.csv")

#Versuch mit kleinerer Datenmenge: Wien Umgebung

#
# AUTmap_Wien = AUTmap.drop(AUTmap[(AUTmap.right < 600000)].index)
# AUTmap_Wien = AUTmap_Wien.drop(AUTmap_Wien[(AUTmap_Wien.top > 460000)].index)
# AUTmap_Wien = AUTmap_Wien.drop(AUTmap_Wien[(AUTmap_Wien.bottom < 400000)].index)
#
#
#
# Points_Wien = gdf.geometry
# tree = STRtree(Points_Wien)
#
# AUTmap_Wien = AUTmap_Wien.assign(AverageDOWNLOAD = 0)
# AUTmap_Wien = AUTmap_Wien.assign(AverageUPLOAD = 0)
#


# #i = 73150
# for p in AUTmap_Wien.geometry:
#
#     res = [x for x in tree.query(p) if p.contains(x)]
#     if len(res) >= 1:
#              i = AUTmap_Wien[AUTmap_Wien['geometry'] == p].index.item()
#              print(i)
#              var = gdf[gdf.isin(res).any(axis=1)]
#              #print(sum(var['download_kbit'])/len(var['download_kbit']))
#
#              AUTmap_Wien.loc[i,'AverageDOWNLOAD'] = sum(var['download_kbit'])/len(var['download_kbit'])
#              AUTmap_Wien.loc[i, 'AverageUPLOAD'] = sum(var['upload_kbit'])/len(var['upload_kbit'])
#
#     #i = i+1
# AUTmap_Wien.to_csv("AUTmapAVERAGES_WienBIG.csv")


#POINT (621684.069 469768.020)







#### QGIS STUFF ###
#gdf.to_csv("Daten_mit_Punkten.csv")  #Erstelle Datei mit bereinigten Daten und Punkten
#EPSG:31287
#AllePunkte  = points.to_csv("AllePunkte.csv")  #Test mit Teil der Punkten

##########################
#PLOTT
# fig, ax = plt.subplots(figsize=(6,6))
# AUTmap.plot(ax=ax, facecolor='blue')
# points.plot(ax=ax, color='red', markersize=5);
# fig.suptitle('Random locations', fontsize=12)
# ax.set_xlabel('Longitude', fontsize=10)
# ax.set_ylabel('Latitude', fontsize='medium')
# plt.show()
###########################







