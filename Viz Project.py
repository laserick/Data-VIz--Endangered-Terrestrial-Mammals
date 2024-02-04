#!/usr/bin/env python
# coding: utf-8

# In[1]:


import geopandas as gpd


# In[2]:


gdf_iucn = gpd.read_file('MAMMALS_TERRESTRIAL_ONLY.zip')
print('Number of records: ', len(gdf_iucn))


# In[3]:


print('Data structure summary:')
print(gdf_iucn.info())


# In[4]:


# Summary statistics for numeric columns
print('Summary statistics for numeric columns:')
print(gdf_iucn.describe())


# In[5]:


# Filter the data
filtered_data = gdf_iucn.drop(columns=["marine","genus","family","class","subspecies","freshwater","citation",
                                      "source","subpop","island","tax_comm","dist_comm","kingdom","phylum",'terrestial'])
target_cat = ['CR', 'LC', 'EN', 'VU', 'NT']
filtered_data = filtered_data[filtered_data['category'].isin(target_cat)]


# In[6]:


filtered_data.info()


# In[7]:


import pandas as pd


# In[8]:


biom_csv = pd.read_csv('species_w_pop_reports_w_ranges_and_gen_length.csv')


# In[9]:


biom_csv.info()
biom_csv = biom_csv['binomial']


# In[10]:


merged_data = filtered_data.merge(biom_csv, left_on='sci_name', right_on='binomial')
merged_data.info()


# In[ ]:





# In[11]:


# Replace 'filtered_data.shp' with the desired file name
# Merged data saved to documents and used for the visualizations in Tableau
merged_data.to_file('C:/Users/Beatrice EvelynKumah/Documents/merge1.shp', driver='ESRI Shapefile')


# In[20]:
############ Trying some visualizations in Python

import matplotlib.pyplot as plt
import seaborn as sns
# Plot a histogram of species count per habitat patch
plt.figure(figsize=(10, 6))
sns.histplot(gdf_iucn['genus']=='Galea', kde=True)
plt.xlabel('Number of Species')
plt.ylabel('Frequency')
plt.title('Species Count Distribution per Habitat Patch')
plt.show()


# In[7]:

# 3. Spatial Visualization
# Plot the habitat patches on a map
plt.figure(figsize=(12, 12))
gdf_iucn.plot(column='genus', cmap='viridis', legend=True)
plt.title('Habitat Patches of Terrestrial Mammals')
plt.axis('off')
plt.show()

# 4. Analyze taxonomic information
# Count species by order and family
species_by_order = gdf_iucn['order'].value_counts()
species_by_family = gdf_iucn['family'].value_counts()

print('Species count by order:')
print(species_by_order)

print('Species count by family:')
print(species_by_family)

# 5. Analyze geospatial features
# Calculate the total area of habitat patches
total_area = gdf_iucn['geometry'].area.sum()
print('Total habitat area (square meters):', total_area)

# 6. Further analysis as per your research objectives

# Remember to save or export your findings and visualizations for reporting.

# Close any open plots
plt.close('all')


# In[9]:


rhinoceros_data = gdf_iucn[gdf_iucn['genus'] == 'Rhinoceros']
rhinoceros_data.plot(marker='o', color='blue', markersize=5, label='Rhinoceros Genus Species')
plt.title("Distribution of Rhinoceros Genus Species")
plt.show()


# In[11]:


taxonomic_counts = rhinoceros_data['order_'].value_counts()
taxonomic_counts.plot(kind='bar', color='lightgreen')
plt.title("Taxonomic Diversity within Rhinoceros Genus")
plt.ylabel("Number of Species")
plt.show()


# In[14]:


import pandas as pd
rhinoceros_data['yrcompiled'] = pd.to_datetime(rhinoceros_data['yrcompiled'])
rhinoceros_data['year'] = rhinoceros_data['yrcompiled'].dt.year
yearly_counts = rhinoceros_data.groupby('year').size()
yearly_counts.plot(kind='line', marker='o', color='blue')
plt.title("Temporal Distribution of Rhinoceros Genus Species")
plt.xlabel("Year")
plt.ylabel("Number of Species")
plt.show()


# In[21]:


# Filter the data for the Rhinoceros genus
rhinoceros_data = gdf_iucn[gdf_iucn['genus'] == 'Rhinoceros']

# Create a map of the Rhinoceros species distribution
rhinoceros_data.plot(marker='o', color='gray', markersize=5, label='Rhinoceros Genus Species')
plt.title("Distribution of Rhinoceros Genus Species")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()





# In[8]:


rhinoceros_data = gdf_iucn[gdf_iucn['genus'] == 'Rhinoceros']
rhinoceros_data.to_file("rhinoceros_data.geojson", driver='GeoJSON')


# In[18]:


import plotly.express as px

# Filter the data for the Rhinoceros genus
rhinoceros_data = gdf_iucn[gdf_iucn['genus'] == 'Rhinoceros']

# Create an interactive map
fig = px.scatter_geo(
    rhinoceros_data,
    lat=rhinoceros_data['geometry'].centroid.y,
    lon=rhinoceros_data['geometry'].centroid.x,
    text=rhinoceros_data['sci_name'],
    title="Distribution of Rhinoceros Genus Species"
)

# Customize the map
fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="Green")

# Show the interactive map
fig.show()

