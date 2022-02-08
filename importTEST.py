import pandas as pd
import geopandas as geo
import matplotlib.pyplot as plt

#Ich habe einen Kommentar hinzugefügt um push zu test lg. bussi

countries_gdf = geo.read_file("Daten/raster_austria.gpkg", rows=10)

print(countries_gdf.geometry)
print(countries_gdf.geometry.name)

#countries_gdf.plot()
countries_gdf.plot()
plt.show()