from .template import Processor


class PeakCalling(Processor):

    bam: str

    def main(
            self,
            bam: str):

        self.bam = bam
