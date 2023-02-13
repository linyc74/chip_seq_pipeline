import os
from typing import Optional, List
from .template import Processor


class PeakCalling(Processor):

    treatment_bam: str
    control_bam: Optional[str]
    macs_effective_genome_size: str
    macs_fdr: float

    peak_files: List[str]

    def main(
            self,
            treatment_bam: str,
            control_bam: Optional[str],
            macs_effective_genome_size: str,
            macs_fdr: float) -> List[str]:

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam
        self.macs_effective_genome_size = macs_effective_genome_size
        self.macs_fdr = macs_fdr

        self.peak_files = []

        self.macs()
        self.homer()

        return self.peak_files

    def macs(self):
        files = MACS(self.settings).main(
            treatment_bam=self.treatment_bam,
            control_bam=self.control_bam,
            effective_genome_size=self.macs_effective_genome_size,
            fdr=self.macs_fdr)
        self.peak_files += files

    def homer(self):
        files = HOMER(self.settings).main(
            treatment_bam=self.treatment_bam,
            control_bam=self.control_bam)
        self.peak_files += files


class MACS(Processor):

    BROAD_CUTOFF = 0.1

    treatment_bam: str
    control_bam: Optional[str]
    effective_genome_size: str
    fdr: float

    dstdir: str
    base_args: List[str]

    def main(
            self,
            treatment_bam: str,
            control_bam: Optional[str],
            effective_genome_size: str,
            fdr: float) -> List[str]:

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam
        self.effective_genome_size = effective_genome_size
        self.fdr = fdr

        self.set_base_args()
        self.call_sharp_peaks()
        self.call_broad_peaks()

        return [
            f'{self.dstdir}/broad_peaks.broadPeak',
            f'{self.dstdir}/sharp_peaks.narrowPeak'
        ]

    def set_base_args(self):
        self.dstdir = f'{self.outdir}/macs2'
        self.base_args = [
            f'macs2 callpeak',
            f'--treatment {self.treatment_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {self.dstdir}',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--qvalue {self.fdr}',
        ]
        if self.control_bam is not None:
            self.base_args += [f'--control {self.control_bam}']

    def call_sharp_peaks(self):
        log = f'{self.outdir}/macs2-callpeak.log'
        args = self.base_args + [
            f'--name sharp',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def call_broad_peaks(self):
        log = f'{self.outdir}/macs2-callpeak-broad.log'
        args = self.base_args + [
            f'--name broad',
            f'--broad',
            f'--broad-cutoff {self.BROAD_CUTOFF}',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))


class HOMER(Processor):

    treatment_bam: str
    control_bam: Optional[str]

    treatment_tag_dir: str
    control_tag_dir: Optional[str]
    dstdir: str
    factor_peaks_txt: str
    histone_regions_txt: str

    def main(
            self,
            treatment_bam: str,
            control_bam: Optional[str]) -> List[str]:

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam

        self.make_treatment_tag_dir()
        self.make_control_tag_dir()
        self.make_dstdir()
        self.find_peaks_factor()
        self.find_peaks_histone()

        return [self.factor_peaks_txt, self.histone_regions_txt]

    def make_treatment_tag_dir(self):
        self.treatment_tag_dir = f'{self.workdir}/treatment-tag'
        self.__make_tag_dir(
            tag_dir=self.treatment_tag_dir,
            bam=self.treatment_bam,
            name='treatment'
        )

    def make_control_tag_dir(self):
        if self.control_bam is None:
            self.control_tag_dir = None
        else:
            self.control_tag_dir = f'{self.workdir}/control-tag'
            self.__make_tag_dir(
                tag_dir=self.control_tag_dir,
                bam=self.control_bam,
                name='control'
            )

    def __make_tag_dir(self, tag_dir: str, bam: str, name: str):
        log = f'{self.outdir}/makeTagDirectory-{name}.log'
        args = [
            'makeTagDirectory',
            tag_dir,
            f'-format sam',
            bam,
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))

    def make_dstdir(self):
        self.dstdir = f'{self.outdir}/homer'
        os.makedirs(self.dstdir, exist_ok=True)

    def find_peaks_factor(self):
        self.factor_peaks_txt = f'{self.dstdir}/factor-peaks.txt'

        args = [
            f'findPeaks',
            self.treatment_tag_dir,
            '-style factor',
            f'-o {self.factor_peaks_txt}'
        ]

        if self.control_tag_dir is not None:
            args += [f'-i {self.control_tag_dir}']

        log = f'{self.outdir}/findPeaks-factor.log'
        args += [
            f'1> {log}',
            f'2> {log}',
        ]

        self.call(self.CMD_LINEBREAK.join(args))

    def find_peaks_histone(self):
        self.histone_regions_txt = f'{self.dstdir}/histone-regions.txt'

        args = [
            f'findPeaks',
            self.treatment_tag_dir,
            '-style histone',
            f'-o {self.histone_regions_txt}'
        ]

        if self.control_tag_dir is not None:
            args += [f'-i {self.control_tag_dir}']

        log = f'{self.outdir}/findPeaks-histone.log'
        args += [
            f'1> {log}',
            f'2> {log}',
        ]

        self.call(self.CMD_LINEBREAK.join(args))
