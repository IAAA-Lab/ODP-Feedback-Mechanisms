import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt


file_path = 'feedback_Testing.xlsx'  # Replace with your actual file path
feedback_df = pd.read_excel(file_path)


country_to_acronym = {
    'Australia': 'AU', 'Austria': 'AT', 'Belgium': 'BE', 'Bulgaria': 'BG',
    'Canada': 'CA', 'Croatia': 'HR', 'Cyprus': 'CY', 'Czech Republic': 'CZ',
    'Denmark': 'DK', 'Estonia': 'EE', 'Finland': 'FI', 'France': 'FR',
    'Germany': 'DE', 'Greece': 'GR', 'Ireland': 'IE', 'Italy': 'IT',
    'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU', 'Malta': 'MT',
    'Netherlands': 'NL', 'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO',
    'Slovakia': 'SK', 'Slovenia': 'SI', 'Spain': 'ES', 'Sweden': 'SE',
    'United States': 'US'
}


feedback_df['Country'] = feedback_df['Country'].str.strip().str.title()  # Remove spaces and standardize case


unmapped_countries = feedback_df[~feedback_df['Country'].isin(country_to_acronym.keys())]
if not unmapped_countries.empty:
    print("Unmapped countries detected. Please update the mapping dictionary with the following:")
    print(unmapped_countries['Country'].unique())


feedback_df['Country'] = feedback_df['Country'].map(country_to_acronym)


if feedback_df['Country'].isna().any():
    print("Some countries could not be mapped to acronyms. Check the dictionary or dataset.")


data_for_clustering = feedback_df.drop(columns=['Country'])


linkage_matrix = linkage(data_for_clustering, method='ward')


correct_threshold = 10  # Adjust based on dendrogram height for 3 clusters


clusters = fcluster(linkage_matrix, t=3, criterion='maxclust')
feedback_df['Cluster'] = clusters


plt.figure(figsize=(10, 6))
dendrogram(
    linkage_matrix,
    labels=feedback_df['Country'].values,  # Use acronyms for labels
    leaf_rotation=90,
    leaf_font_size=10,
    color_threshold=correct_threshold  # Ensure consistent 3 colors
)
plt.axhline(y=correct_threshold, color='r', linestyle='--', label='Cut-off for 3 Clusters')
plt.title("Dendrogram with 3 Clusters (Acronyms)")
plt.xlabel("Countries")
plt.ylabel("Euclidean Distance")
plt.legend()
plt.savefig("Dendrogram_3_Clusters_Acronyms_Fixed.pdf", format='pdf')
plt.show()
