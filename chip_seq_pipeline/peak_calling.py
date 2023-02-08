from .template import Processor


class PeakCalling(Processor):

    treatment_bam: str
    control_bam: str
    peak_caller: str

    def main(
            self,
            treatment_bam: str,
            control_bam: str,
            peak_caller: str):

        self.treatment_bam = treatment_bam
        self.control_bam = control_bam
        self.peak_caller = peak_caller
