import time
import random
from typing import List
from os.path import basename
from multiprocessing import Pool
from .template import Processor


class MotifFinding(Processor):

    peak_files: List[str]
    genome_version: str
    fragment_size: int

    def main(
            self,
            peak_files: List[str],
            genome_version: str,
            fragment_size: int):

        self.peak_files = peak_files
        self.genome_version = genome_version
        self.fragment_size = fragment_size

        with Pool(self.threads) as p:
            p.map(self.find_motifs_genome, self.peak_files)

    def find_motifs_genome(self, peak_file: str):
        time.sleep(random.random())  # to avoid concurrent log message
        FindMotifsGenome(self.settings).main(
            peak_file=peak_file,
            genome_version=self.genome_version,
            fragment_size=self.fragment_size)


class FindMotifsGenome(Processor):

    peak_file: str
    genome_version: str
    fragment_size: int

    def main(
            self,
            peak_file: str,
            genome_version: str,
            fragment_size: int):

        self.peak_file = peak_file
        self.genome_version = genome_version
        self.fragment_size = fragment_size

        self.execute()
        self.print_done_msg()

    def execute(self):
        outdir = f'{self.peak_file}-findMotifsGenome'
        log = f'{self.outdir}/findMotifsGenome-[{basename(self.peak_file)}].log'
        args = [
            f'findMotifsGenome.pl',
            self.peak_file,
            self.genome_version,
            f'{outdir}',
            f'-size {self.fragment_size}',
            '-mask',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def print_done_msg(self):
        self.logger.info(f'findMotifsGenome.pl done for: {self.peak_file}')
