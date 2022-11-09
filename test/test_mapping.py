from chip_seq_pipeline.mapping import Mapping
from .setup import TestCase


class TestMapping(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_bwa_paired_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=f'{self.indir}/tumor.2.fq.gz',
            read_aligner='bwa',
            bowtie2_mode='sensitive',
            discard_bam=True
        )
        expected = f'{self.workdir}/sorted.bam'
        self.assertFileExists(expected, actual)

    def test_bwa_single_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=None,
            read_aligner='bwa',
            bowtie2_mode='sensitive',
            discard_bam=True
        )
        expected = f'{self.workdir}/sorted.bam'
        self.assertFileExists(expected, actual)

    def test_bowtie2_paired_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=f'{self.indir}/tumor.2.fq.gz',
            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False
        )
        expected = f'{self.outdir}/sorted.bam'
        self.assertFileExists(expected, actual)

    def test_bowtie2_single_end(self):
        actual = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=None,
            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False
        )
        expected = f'{self.outdir}/sorted.bam'
        self.assertFileExists(expected, actual)