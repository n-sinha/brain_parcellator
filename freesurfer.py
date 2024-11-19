import os
import subprocess
import json
import argparse
import shutil

class Multiscaleatlas:
    def __init__(self, t1, subjectID, output_dir=None):
        self.t1 = t1
        self.subjectID = subjectID
        self.output_dir = output_dir
        self.setup_environment()  # Call setup_environment during initialization

    def setup_environment(self):
        with open('setup_environment.json', 'r') as f:
            env_vars = json.load(f)
        
        for key, value in env_vars.items():
            os.environ[key] = value

        FREESURFER_HOME = os.environ['FREESURFER_HOME']
        freesurferdirmpath = f'{FREESURFER_HOME}/SetUpFreeSurfer.sh'

        # Execute the setup script
        subprocess.run(['sh', freesurferdirmpath], check=True)

    def recon_all(self):
        '''
        Run recon-all command to generate the freesurfer reconstructions
        '''   
        cmd = ['recon-all', 
               '-s', self.subjectID,
               '-i', self.t1,
               '-threads', '8', '-all']
        subprocess.run(cmd, check=True)

    def lausanne2018scale1(self):
        '''Run Lausanne 2018 Scale 1 parcellation'''
        sub_dir = os.environ.get('SUBJECTS_DIR')

        # Surface-to-Surface Mapping for Left Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'lh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/lh.lausanne2018.scale1.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/lh.lausanne2018.scale1.annot')]
        
        subprocess.run(cmd, check=True)

        # Surface-to-Surface Mapping for Right Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'rh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/rh.lausanne2018.scale1.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/rh.lausanne2018.scale1.annot')]
        
        subprocess.run(cmd, check=True)

        # Anatomical Statistics for Left Hemisphere
        cmd = ['mris_anatomical_stats', 
               '-th3', '-mgz', '-noglobal',
               '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'lh.cortex.label'),
               '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'lh.lausanne2018.scale1.stats'),
               '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'lh.lausanne2018.scale1.annot'),
               self.subjectID, 'lh']

        subprocess.run(cmd, check=True)

        # Anatomical Statistics for Right Hemisphere
        cmd = ['mris_anatomical_stats', 
               '-th3', '-mgz', '-noglobal',
               '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'rh.cortex.label'),
               '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'rh.lausanne2018.scale1.stats'),
               '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'rh.lausanne2018.scale1.annot'),
               self.subjectID, 'rh']

        subprocess.run(cmd, check=True)

        # Convert Aparc to Aseg
        cmd = ['mri_aparc2aseg',
        '--old-ribbon',
               '--s', self.subjectID,
               '--annot', 'lausanne2018.scale1',
               '--threads', '8',
               '--o', os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale1.mgz')]
        
        subprocess.run(cmd, check=True)

        # Convert MGZ to NII format
        cmd = ['mri_convert',
               os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale1.mgz'),
               os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale1.nii.gz')]
        
        subprocess.run(cmd, check=True)
    
    def lausanne2018scale2(self):
        '''Run Lausanne 2018 Scale 2 parcellation'''
            
        sub_dir = os.environ.get('SUBJECTS_DIR')
    
        # Surface-to-Surface Mapping for Left Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'lh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/lh.lausanne2018.scale2.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/lh.lausanne2018.scale2.annot')]
            
        subprocess.run(cmd, check=True)
    
        # Surface-to-Surface Mapping for Right Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'rh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/rh.lausanne2018.scale2.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/rh.lausanne2018.scale2.annot')]
            
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Left Hemisphere
        cmd = ['mris_anatomical_stats', '-th3', '-mgz', '-noglobal',
                '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'lh.cortex.label'),
                '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'lh.lausanne2018.scale2.stats'),
                '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'lh.lausanne2018.scale2.annot'),
                self.subjectID, 'lh']
    
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Right Hemisphere
        cmd = ['mris_anatomical_stats', 
                '-th3', '-mgz', '-noglobal',
                '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'rh.cortex.label'),
                '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'rh.lausanne2018.scale2.stats'),
                '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'rh.lausanne2018.scale2.annot'),
                self.subjectID, 'rh']
            
        subprocess.run(cmd, check=True)

        # Convert Aparc to Aseg
        cmd = ['mri_aparc2aseg', 
                '--old-ribbon',
                '--s', self.subjectID,
                '--annot', 'lausanne2018.scale2',
                '--threads', '8',
                '--o', os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale2.mgz')]
            
        subprocess.run(cmd, check=True)

            # Convert MGZ to NII format
        cmd = ['mri_convert',
                os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale2.mgz'),
                os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale2.nii.gz')]
            
        subprocess.run(cmd, check=True)

    def lausanne2018scale3(self):
        '''Run Lausanne 2018 Scale 3 parcellation'''
        sub_dir = os.environ.get('SUBJECTS_DIR')

        # Surface-to-Surface Mapping for Left Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'lh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/lh.lausanne2018.scale3.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/lh.lausanne2018.scale3.annot')]
        
        subprocess.run(cmd, check=True)

        # Surface-to-Surface Mapping for Right Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'rh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/rh.lausanne2018.scale3.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/rh.lausanne2018.scale3.annot')]
        
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Left Hemisphere
        cmd = ['mris_anatomical_stats', 
            '-th3', '-mgz', '-noglobal',
            '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'lh.cortex.label'),
            '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'lh.lausanne2018.scale3.stats'),
            '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'lh.lausanne2018.scale3.annot'),
            self.subjectID, 'lh']
    
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Right Hemisphere
        cmd = ['mris_anatomical_stats', 
            '-th3', '-mgz', '-noglobal',
            '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'rh.cortex.label'),
            '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'rh.lausanne2018.scale3.stats'),
            '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'rh.lausanne2018.scale3.annot'),
            self.subjectID, 'rh']
        
        subprocess.run(cmd, check=True)

        # Convert Aparc to Aseg
        cmd = ['mri_aparc2aseg', 
            '--old-ribbon',
            '--s', self.subjectID,
            '--annot', 'lausanne2018.scale3',
            '--threads', '8',
            '--o', os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale3.mgz')]
        
        subprocess.run(cmd, check=True)

        # Convert MGZ to NII format
        cmd = ['mri_convert',
            os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale3.mgz'),
            os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale3.nii.gz')]
        
        subprocess.run(cmd, check=True)

    def lausanne2018scale4(self):
        '''Run Lausanne 2018 Scale 4 parcellation'''

        sub_dir = os.environ.get('SUBJECTS_DIR')

        # Surface-to-Surface Mapping for Left Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'lh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/lh.lausanne2018.scale4.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/lh.lausanne2018.scale4.annot')]
        
        subprocess.run(cmd, check=True)

            # Surface-to-Surface Mapping for Right Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'rh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/rh.lausanne2018.scale4.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/rh.lausanne2018.scale4.annot')]
            
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Left Hemisphere
        cmd = ['mris_anatomical_stats', 
                '-th3', '-mgz', '-noglobal',
                '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'lh.cortex.label'),
                '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'lh.lausanne2018.scale4.stats'),
                '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'lh.lausanne2018.scale4.annot'),
                self.subjectID, 'lh']
        
        subprocess.run(cmd, check=True)
    
        # Anatomical Statistics for Right Hemisphere
        cmd = ['mris_anatomical_stats', 
                '-th3', '-mgz', '-noglobal',
                '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'rh.cortex.label'),
                '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'rh.lausanne2018.scale4.stats'),
                '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'rh.lausanne2018.scale4.annot'),
                self.subjectID, 'rh']
        
        subprocess.run(cmd, check=True)

        # Convert Aparc to Aseg
        cmd = ['mri_aparc2aseg', 
                '--old-ribbon',
                '--s', self.subjectID,
                '--annot', 'lausanne2018.scale4',
                '--threads', '8',
                '--o', os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale4.mgz')]
        
        subprocess.run(cmd, check=True)

        # Convert MGZ to NII format
        cmd = ['mri_convert',
                os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale4.mgz'),
                os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale4.nii.gz')]
            
        subprocess.run(cmd, check=True)

    def lausanne2018scale5(self):
        '''Run Lausanne 2018 Scale 5 parcellation'''
        sub_dir = os.environ.get('SUBJECTS_DIR')

        # Surface-to-Surface Mapping for Left Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'lh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/lh.lausanne2018.scale5.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/lh.lausanne2018.scale5.annot')]
        
        subprocess.run(cmd, check=True)

        # Surface-to-Surface Mapping for Right Hemisphere
        cmd = ['mri_surf2surf',
                '--srcsubject', 'fsaverage',
                '--trgsubject', self.subjectID,
                '--hemi', 'rh',
                '--sval-annot', os.path.join(sub_dir, 'fsaverage/label/rh.lausanne2018.scale5.annot'),
                '--tval', os.path.join(sub_dir, self.subjectID, 'label/rh.lausanne2018.scale5.annot')]
        
        subprocess.run(cmd, check=True)

        # Anatomical Statistics for Left Hemisphere
        cmd = ['mris_anatomical_stats', 
            '-th3', '-mgz', '-noglobal',
            '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'lh.cortex.label'),
            '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'lh.lausanne2018.scale5.stats'),
            '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'lh.lausanne2018.scale5.annot'),
            self.subjectID, 'lh']

        subprocess.run(cmd, check=True)

        # Anatomical Statistics for Right Hemisphere
        cmd = ['mris_anatomical_stats', 
            '-th3', '-mgz', '-noglobal',
            '-cortex', os.path.join(sub_dir, self.subjectID, 'label', 'rh.cortex.label'),
            '-f', os.path.join(sub_dir, self.subjectID, 'stats', 'rh.lausanne2018.scale5.stats'),
            '-b', '-a', os.path.join(sub_dir, self.subjectID, 'label', 'rh.lausanne2018.scale5.annot'),
            self.subjectID, 'rh']
        
        subprocess.run(cmd, check=True)

        # Convert Aparc to Aseg
        cmd = ['mri_aparc2aseg', 
            '--old-ribbon',
            '--s', self.subjectID,
            '--annot', 'lausanne2018.scale5',
            '--threads', '8',
            '--o', os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale5.mgz')]
        
        subprocess.run(cmd, check=True)

        # Convert MGZ to NII format
        cmd = ['mri_convert',
            os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale5.mgz'),
            os.path.join(sub_dir, self.subjectID, 'mri', 'lausanne2018.scale5.nii.gz')]
        
        subprocess.run(cmd, check=True)

    def move_output(self):
        '''move the output directory to the desired location'''
        if self.output_dir:
            source_dir = os.path.join(os.environ.get('SUBJECTS_DIR'), self.subjectID)
            output_dir = self.output_dir
            shutil.move(source_dir, output_dir)


def main():
    parser = argparse.ArgumentParser(description='Run Freesurfer recon-all.')
    parser.add_argument('-t1', type=str, required=True, help='Path to the T1 image (required)', metavar='')
    parser.add_argument('-s', type=str, required=True, help='Subject ID (required)',metavar='')
    parser.add_argument('-o', type=str, help='Output directory (optional)', metavar='')
    args = parser.parse_args()

    recon = Multiscaleatlas(args.t1, args.s, args.o)
    recon.recon_all()
    recon.lausanne2018scale1()
    recon.lausanne2018scale2()
    recon.lausanne2018scale3()
    recon.lausanne2018scale4()
    recon.lausanne2018scale5()
    recon.move_output()

if __name__ == "__main__":
    main()

