from typing import List
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
        args = [
            'annotatePeaks.pl',
            peak_file,
            self.genome_version,
            f'1> {out}',
            f'2> {self.outdir}/annotatePeaks.log',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def __add_suffix_to_fname(self, f: str) -> str:
        p = f.rfind('.')
        prefix = f[:p]
        suffix = f[p+1:]
        return f'{prefix}-{self.FNAME_SUFFIX}.{suffix}'
