import datetime
from pathlib import Path
import subprocess

def create_log():
    output_filename = f'{datetime.datetime.today():%Y-%m-%d_%H%M}'
    output_filename_md = f'{output_filename}.md'
    output_filename_pdf = f'{output_filename}.pdf'
    output_filepath_md = Path().cwd()/'call_logs'/f'{output_filename_md}' 
    output_filepath_pdf = Path().cwd()/'call_logs'/f'{output_filename_pdf}' 

    with open(output_filepath_md, 'wt') as file:
        file.write(f'# Chat log\n')
        file.write(f'### Support call worker ID: Jack Daws\n')
        file.write(f'### Customer ID: 1542\n')
    subprocess.call(f"mdpdf -o {output_filepath_pdf} {output_filepath_md}", shell=True)

if __name__ == '__main__':
    create_log()