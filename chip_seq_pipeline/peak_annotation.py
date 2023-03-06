from typing import List
from os.path import basename
from .template import Processor


class PeakAnnotation(Processor):

    FNAME_SUFFIX = 'annotated'

    peak_files: List[str]
    genome_version: str

    def main(self, peak_files: List[str], genome_version: str):

        self.peak_files = peak_files
        self.genome_version = genome_version

        for peak_file in self.peak_files:
            self.annotate(peak_file)

    def annotate(self, peak_file: str):
        out = self.__add_suffix_to_fname(peak_file)
        log = f'{self.outdir}/annotatePeaks-[{basename(peak_file)}].log'
        args = [
            'annotatePeaks.pl',
            peak_file,
            self.genome_version,
            f'1> {out}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def __add_suffix_to_fname(self, f: str) -> str:
        p = f.rfind('.')
        prefix = f[:p]
        suffix = f[p+1:]
        return f'{prefix}-{self.FNAME_SUFFIX}.{suffix}'
