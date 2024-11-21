import os
import pandas as pd
from bids2table import bids2table

class getfiles:
    def __init__(self, BIDS_path):
        self.BIDS_path = BIDS_path
        self.BIDS_df = bids2table(self.BIDS_path)

    def locT1w(self):
        """
        Get the location of T1w images for all subjects in the BIDS dataset
        """
        bidsdf = self.BIDS_df.filter_multi(
            suffix="T1w",
            ses={"items": ["research3T", "clinical01"]}
        )
        bidsdf = bidsdf.flat

        # drop the columns that are all missing
        bidsdf = bidsdf.dropna(axis=1, how='all')

        # if a subject has both clinical and reasearch T1w, keep the research T1w
        duplicates = bidsdf[bidsdf.duplicated(subset='sub', keep=False)]
        duplicates_resolved = duplicates[duplicates['ses'] != 'clinical01']

        cleaned = pd.concat([duplicates_resolved, bidsdf[~bidsdf.duplicated(subset='sub', keep=False)]])
        cleaned = cleaned.sort_values(by='sub').reset_index(drop=True)

        fs_reconall = cleaned.drop(columns=['extra_entities', 'json', 'space', 'mod_time'])
        return fs_reconall
    
    def locdwi(self):
        """
        Get the location of dwi images for all subjects in the BIDS dataset
        """
        bidsdf = self.BIDS_df.filter_multi(
            suffix="dwi",
            ses={"items": ["research3T", "clinical01"]}
        )
        bidsdf = bidsdf.flat
        
        # drop the columns that are all missing
        bidsdf = bidsdf.dropna(axis=1, how='all')
        bidsdf = bidsdf[bidsdf['run'] != 1] # assuming the first run was not complete and run 2 is the complete one

        dwi = bidsdf.pivot_table(index='sub', columns='ext', values='file_path', aggfunc='first')

        # rename coloums names
        dwi.columns = ['bval', 'bvec', 'dwi']

        return dwi
    
    def loctopup(self):
        """
        Get the location of topup images for all subjects in the BIDS dataset
        """
        bidsdf = self.BIDS_df.filter_multi(
            suffix="epi",
            ext = ".nii.gz",
            ses={"items": ["research3T", "clinical01"]}
        )
        bidsdf = bidsdf.flat
        
        # drop the columns that are all missing
        bidsdf = bidsdf.dropna(axis=1, how='all')
        bidsdf = bidsdf[bidsdf['run'] != 1]  # assuming the first run was not complete and run 2 is the complete one

        topup = bidsdf.pivot_table(index='sub', columns='ext', values='file_path', aggfunc='first')

        # rename coloums
        topup.columns = ['topup']

        return topup


def main():
    BIDS_path = '/project/davis_group_1/nishants/epi_t3_iEEG/data/BIDS'
    files = getfiles(BIDS_path)
    fs_reconall = files.locT1w()
    fs_reconall['sub'] = 'sub-' + fs_reconall['sub']
    # export only sub and filepath columns
    fs_reconall.to_csv('/project/davis_group_1/nishants/brain_parcellator/jobs/fs_reconall.csv',
                        columns=['sub', 'file_path'], index=False, header=False)

if __name__ == "__main__":
    main()
