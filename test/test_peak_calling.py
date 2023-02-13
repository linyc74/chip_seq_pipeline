from chip_seq_pipeline.peak_calling import PeakCalling
from .setup import TestCase


class TestPeakCalling(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_treatment_control(self):
        PeakCalling(self.settings).main(
            treatment_bam=f'{self.indir}/sorted-treatment.bam',
            control_bam=f'{self.indir}/sorted-control.bam',
            effective_genome_size='5.1e7',  # size of chr22
            fdr=0.05
        )

    def test_treatment_only(self):
        PeakCalling(self.settings).main(
            treatment_bam=f'{self.indir}/sorted-treatment.bam',
            control_bam=None,
            effective_genome_size='5.1e7',  # size of chr22
            fdr=0.05
        )
