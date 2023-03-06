from typing import List
from os.path import basename
from .template import Processor


class MotifFinding(Processor):

    peak_files: List[str]
    genome_version: str

    def main(self, peak_files: List[str], genome_version: str):

        self.peak_files = peak_files
        self.genome_version = genome_version

        for peak_file in self.peak_files:
            FindMotifsGenome(self.settings).main(
                peak_file=peak_file,
                genome_version=self.genome_version)


class FindMotifsGenome(Processor):

    SIZE = 200

    peak_file: str
    genome_version: str

    def main(self, peak_file: str, genome_version: str):

        self.peak_file = peak_file
        self.genome_version = genome_version

        outdir = f'{self.peak_file}-findMotifsGenome'
        log = f'{self.outdir}/findMotifsGenome-[{basename(peak_file)}].log'
        args = [
            f'findMotifsGenome.pl',
            self.peak_file,
            genome_version,
            f'{outdir}',
            f'-size {self.SIZE}',
            '-mask',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))
