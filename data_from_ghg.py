# -*- coding: utf-8 -*-
"""
Created on Wed Aug 20 14:17:57 2025

@author: David Trejo Cancino
"""

import zipfile
import pandas as pd
import os
#%% Functions

def biomet_from_ghg(root_dir):
    """
    Walks through all the directories and ghg files and returns the biomet data
    from them as a DataFrame.

    Parameters
    ----------
    foot_dir : str
        Root directory as a string.

    Returns
    -------
    biomet_dfs : DataFrame
        Biomet data coming from the ghg files.

    """
    # Create a list to collect all biomet data DataFrames
    biomet_dfs = []
    # Walk through all directories and files
    for dirpath, dirnames, filenames in os.walk(root_dir+"/"):
        for filename in filenames:
            if filename.lower().endswith(".ghg"):
                ghg_path = os.path.join(dirpath, filename)
                try:
                    with zipfile.ZipFile(ghg_path, 'r') as z:
                        biomet_file = next((f for f in z.namelist() if 'biomet.data' in f), None)
                        if biomet_file:
                            with z.open(biomet_file) as f:
                                df = pd.read_csv(f, skiprows=5, sep="\t")  
                                # df["source_file"] = filename  # add column to trace origin
                                biomet_dfs.append(df)
                        else:
                            print(f"No biomet.data found in {filename}")
                except zipfile.BadZipFile:
                    print(f"Corrupted file or not a zip: {ghg_path}")
                except pd.errors.ParserError:
                    print(f"ParseError in {filename}")
    
    # Combine all DataFrames into one
    if biomet_dfs:
        all_biomet_data = pd.concat(biomet_dfs, ignore_index=True)
        print(all_biomet_data.head())

    else:
        print("No biomet data found in any .ghg files.")
    return biomet_dfs

#%% Example of usage
"""
Depending on the amount of ghg files the process could take some time

"""
# Set the root directory to search for .ghg files
root_dir = r"C:/Users/JohnDoe/EC Data"
biomet_df = biomet_from_ghg(root_dir)

