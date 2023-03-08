from typing import Optional
from os.path import basename, exists
from .template import Processor


class Bam2BigWig(Processor):

    treatment_bam: str
    control_bam: Optional[str]

    def main(self,  treatment_bam: str, control_bam: str):

        self.control_bam = control_bam
        self.treatment_bam = treatment_bam

        self.index_bam()
        self.bam_coverage()

    def index_bam(self):
        for bam in [self.treatment_bam, self.control_bam]:
            if bam is not None:
                bai = f'{bam}.bai'
                if not exists(bai):
                    self.call(f'samtools index {bam}')

    def bam_coverage(self):
        for bam in [self.treatment_bam, self.control_bam]:
            if bam is not None:
                BamCoverage(self.settings).main(bam=bam)


class BamCoverage(Processor):

    BIN_SIZE = 10

    bam: str

    bigwig: str

    def main(self, bam: str) -> str:

        self.bam = bam

        log = f'{self.outdir}/bamCoverage-[{basename(self.bam)}].log'
        self.bigwig = f'{self.outdir}/{basename(self.bam).replace(".bam", ".bw")}'
        args = [
            'bamCoverage',
            f'--bam {self.bam}',
            f'--outFileName {self.bigwig}',
            f'--numberOfProcessors {self.threads}',
            f'--binSize {self.BIN_SIZE}',
            '--outFileFormat bigwig',
            '--normalizeUsing None',
            '--ignoreDuplicates',
            '--centerReads',
            f'1> {log}',
            f'2> {log}'
        ]
        self.call(self.CMD_LINEBREAK.join(args))

        return self.bigwig
