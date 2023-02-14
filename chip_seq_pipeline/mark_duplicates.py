import os
from typing import Optional, Tuple
from .tools import edit_fpath
from .template import Processor


class MarkDuplicates(Processor):

    treatment_bam: str
    control_bam: Optional[str]

    out_treatment_bam: str
    out_control_bam: Optional[str]

    def main(
            self,
            treatment_bam: str,
            control_bam: Optional[str]) -> Tuple[str, Optional[str]]:

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam

        self.out_treatment_bam = GATKMarkDuplicates(self.settings).main(
            bam=self.treatment_bam)

        self.out_control_bam = None if self.control_bam is None else \
            GATKMarkDuplicates(self.settings).main(bam=self.control_bam)

        return self.out_treatment_bam, self.out_control_bam


class GATKMarkDuplicates(Processor):

    REMOVE_DUPLICATES = 'false'
    METRICS_DIRNAME = 'duplicate-metrics'

    bam: str

    metrics_txt: str
    out_bam: str

    def main(self, bam: str) -> str:
        self.bam = bam
        self.set_out_bam()
        self.set_metrics_txt()
        self.execute()
        return self.out_bam

    def set_out_bam(self):
        self.out_bam = edit_fpath(
            fpath=self.bam,
            old_suffix='.bam',
            new_suffix='-mark-duplicates.bam',
            dstdir=self.workdir)

    def set_metrics_txt(self):
        dstdir = f'{self.outdir}/{self.METRICS_DIRNAME}'
        os.makedirs(dstdir, exist_ok=True)
        self.metrics_txt = edit_fpath(
            fpath=self.bam,
            old_suffix='.bam',
            new_suffix='-duplicate-metrics.txt',
            dstdir=dstdir)

    def execute(self):
        log = f'{self.outdir}/gatk-MarkDuplicates.log'
        cmd = self.CMD_LINEBREAK.join([
            'gatk MarkDuplicates',
            f'--INPUT {self.bam}',
            f'--METRICS_FILE {self.metrics_txt}',
            f'--OUTPUT {self.out_bam}',
            f'--REMOVE_DUPLICATES {self.REMOVE_DUPLICATES}',
            f'1>> {log}',
            f'2>> {log}',
        ])
        self.call(cmd)
