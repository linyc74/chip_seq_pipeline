from typing import Optional
from .template import Processor


class PeakCalling(Processor):

    # MACS
    BROAD_CUTOFF = 0.1

    # HOMER

    treatment_bam: str
    control_bam: Optional[str]
    effective_genome_size: str
    fdr: float

    def main(
            self,
            treatment_bam: str,
            control_bam: str,
            effective_genome_size: str,
            fdr: float):

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam
        self.effective_genome_size = effective_genome_size
        self.fdr = fdr

        if self.control_bam is not None:
            self.macs_treatment_control_sharp()
            self.macs_treatment_control_broad()
            self.homer_treatment_control_sharp()
            self.homer_treatment_control_broad()
        else:
            self.macs_treatment_only_sharp()
            self.macs_treatment_only_broad()
            self.homer_treatment_only_sharp()
            self.homer_treatment_only_broad()

    def macs_treatment_control_sharp(self):
        log = f'{self.outdir}/macs2-callpeak.log'
        outdir = f'{self.outdir}/macs2'
        args = [
            f'macs2 callpeak',
            f'--treatment {self.treatment_bam}',
            f'--control {self.control_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {outdir}',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--qvalue {self.fdr}',
            f'--name sharp',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def macs_treatment_control_broad(self):
        log = f'{self.outdir}/macs2-callpeak-broad.log'
        outdir = f'{self.outdir}/macs2'
        args = [
            f'macs2 callpeak --broad',
            f'--treatment {self.treatment_bam}',
            f'--control {self.control_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {outdir}',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--broad-cutoff {self.BROAD_CUTOFF}',
            f'--qvalue {self.fdr}',
            f'--name broad',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def macs_treatment_only_sharp(self):
        log = f'{self.outdir}/macs2-callpeak.log'
        outdir = f'{self.outdir}/macs2'
        args = [
            f'macs2 callpeak',
            f'--treatment {self.treatment_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {outdir}',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--qvalue {self.fdr}',
            f'--name sharp',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def macs_treatment_only_broad(self):
        log = f'{self.outdir}/macs2-callpeak-broad.log'
        outdir = f'{self.outdir}/macs2'
        args = [
            f'macs2 callpeak --broad',
            f'--treatment {self.treatment_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {outdir}',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--broad-cutoff {self.BROAD_CUTOFF}',
            f'--qvalue {self.fdr}',
            f'--name broad',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def homer_treatment_control_sharp(self):
        pass

    def homer_treatment_control_broad(self):
        pass

    def homer_treatment_only_sharp(self):
        pass

    def homer_treatment_only_broad(self):
        pass
