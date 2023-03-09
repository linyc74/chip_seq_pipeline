import time
import random
import pandas as pd
from os.path import basename
from multiprocessing import Pool
from typing import List, Dict, Union, Optional
from .template import Processor


class ChIPseeker(Processor):

    peak_files: List[str]

    def main(self, peak_files: List[str]):
        self.peak_files = peak_files

        with Pool(self.threads) as p:
            p.map(self.covplot, self.peak_files)

    def covplot(self, peak_file: str):
        time.sleep(random.random())  # to avoid concurrent log message
        CovPlot(self.settings).main(peak_file=peak_file)


class CovPlot(Processor):

    peak_file: str

    clean_bed: Optional[str]

    def main(self, peak_file: str):
        self.peak_file = peak_file

        self.write_clean_bed()
        if self.clean_bed is None:
            self.skip_message()
            return
        self.run_covplot_r_script()
        self.done_message()

    def skip_message(self):
        self.logger.info(f'Skip empty peak file: {self.peak_file}')

    def write_clean_bed(self):
        self.clean_bed = WriteCleanBed(self.settings).main(
            peak_file=self.peak_file)

    def run_covplot_r_script(self):
        RunCovPlotRScript(self.settings).main(
            peak_file=self.peak_file,
            clean_bed=self.clean_bed)

    def done_message(self):
        self.logger.info(f'ChIPseeker covplot done for: {self.peak_file}')


class WriteCleanBed(Processor):

    VALID_CHR_PREFIX = 'chr'

    peak_file: str

    is_homer_format: bool  # otherwise it's MACS format
    data: List[
        Dict[str, Union[str, int]]
    ]
    clean_bed: str

    def main(self, peak_file: str) -> Optional[str]:

        self.peak_file = peak_file

        self.tell_if_is_homer_format()
        self.parse_lines_and_set_data()
        if len(self.data) == 0:
            return None
        self.write_clean_bed()

        return self.clean_bed

    def tell_if_is_homer_format(self):
        self.is_homer_format = False
        with open(self.peak_file) as fh:
            for line in fh:
                if line.startswith('#PeakID'):
                    self.is_homer_format = True
                    break

    def parse_lines_and_set_data(self):
        self.data = []
        with open(self.peak_file) as fh:
            for line in fh:
                self.__parse_one_(line)

    def __parse_one_(self, line: str):
        if line.startswith('#'):
            return

        items = line.split('\t')

        if self.is_homer_format:  # PeakID, chr, start, end, strand, Normalized
            chr_, start, end = items[1:4]
            weight = items[5]
        else:  # chr, start, end, peak_id, weight
            chr_, start, end = items[0:3]
            weight = items[4]

        if not chr_.startswith(self.VALID_CHR_PREFIX):
            return

        self.data.append({
            'chr': chr_,
            'start': int(start),
            'end': int(end),
            'weight': float(weight),
        })

    def write_clean_bed(self):
        fname = get_filename(path=self.peak_file, dirpath=False, extension=False)
        self.clean_bed = f'{self.workdir}/clean-{fname}.bed'

        pd.DataFrame(
            data=self.data
        ).sort_values(
            by=['chr', 'start']
        ).to_csv(
            self.clean_bed,
            sep='\t',
            index=False,
            header=False
        )


class RunCovPlotRScript(Processor):

    peak_file: str
    clean_bed: str

    r_script: str

    def main(self, peak_file: str, clean_bed: str):

        self.peak_file = peak_file
        self.clean_bed = clean_bed

        self.set_r_script()
        self.run_r_script()

    def set_r_script(self):
        pdf = get_filename(path=self.peak_file, dirpath=True, extension=False) + '.pdf'
        weight_col = 'V4'  # 4th field without column name

        self.r_script = f'''\
  library(ChIPseeker)
  peaks <- readPeakFile("{self.clean_bed}")
  pdf("{pdf}")
  covplot(peaks, weightCol="{weight_col}")'''

    def run_r_script(self):
        f = get_filename(path=self.peak_file, dirpath=False, extension=False)

        r_file = f'{self.workdir}/covplot-[{f}].R'

        with open(r_file, 'w') as fh:
            fh.write(self.r_script)

        self.logger.info(f'"{r_file}"\n{self.r_script}')

        log = f'{self.outdir}/covplot-[{f}].log'
        cmd = self.CMD_LINEBREAK.join([
            'Rscript',
            r_file,
            f'1> {log}',
            f'2> {log}'
        ])
        self.call(cmd)


def get_filename(path: str, dirpath: bool, extension: bool):

    if not dirpath:
        path = basename(path)

    if not extension:
        path = path.rsplit('.', 1)[0]

    return path
