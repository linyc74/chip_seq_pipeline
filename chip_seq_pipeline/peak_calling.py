from .template import Processor


class PeakCalling(Processor):

    treatment_bam: str
    control_bam: str
    peak_caller: str
    effective_genome_size: str
    fdr: float

    def main(
            self,
            treatment_bam: str,
            control_bam: str,
            peak_caller: str,
            effective_genome_size: str,
            fdr: float):

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam
        self.peak_caller = peak_caller
        self.effective_genome_size = effective_genome_size
        self.fdr = fdr

        log = f'{self.outdir}/macs2-callpeak.log'
        args = [
            f'macs2 callpeak',
            f'--treatment {self.treatment_bam}',
            f'--control {self.control_bam}',
            f'--format BAMPE',  # BAM paired-end reads
            f'--gsize {self.effective_genome_size}',
            f'--outdir {self.outdir}',
            f'--name test',
            f'--bdg',  # save extended fragment pileup, and local lambda tracks (two files) at every bp into a bedGraph file
            f'--qvalue {self.fdr}',
            f'1> {log}',
            f'2> {log}',
        ]
        self.call(self.CMD_LINEBREAK.join(args))
