import time
import random
from typing import List
from os.path import basename
from multiprocessing import Pool
from .template import Processor


class PeakAnnotation(Processor):

    peak_files: List[str]
    genome_version: str

    def main(self, peak_files: List[str], genome_version: str):

        self.peak_files = peak_files
        self.genome_version = genome_version

        with Pool(self.threads) as p:
            p.map(self.anntotate_peaks, self.peak_files)

    def anntotate_peaks(self, peak_file: str):
        time.sleep(random.random())  # to avoid concurrent log message
        AnnotatePeaks(self.settings).main(
            peak_file=peak_file,
            genome_version=self.genome_version)


class AnnotatePeaks(Processor):

    FNAME_SUFFIX = 'annotated.tsv'

    peak_file: str
    genome_version: str

    out_file: str

    def main(self, peak_file: str, genome_version: str) -> str:

        self.peak_file = peak_file
        self.genome_version = genome_version

        self.set_out_file()
        self.annotate()

        return self.out_file

    def set_out_file(self):
        prefix = self.peak_file.rsplit('.', 1)[0]
        self.out_file = f'{prefix}-{self.FNAME_SUFFIX}'

    def annotate(self):
        log = f'{self.outdir}/annotatePeaks-[{basename(self.peak_file)}].log'
        args = [
            'annotatePeaks.pl',
            self.peak_file,
            self.genome_version,
            f'1> {self.out_file}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))
