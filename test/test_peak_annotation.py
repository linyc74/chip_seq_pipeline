import shutil
from os.path import exists
from chip_seq_pipeline.peak_annotation import PeakAnnotation
from .setup import TestCase


class TestPeakAnnotation(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)
        self.settings.threads = 2  # to avoid memory overload

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        self.__move_test_files_to_outdir()

        PeakAnnotation(self.settings).main(
            peak_files=[
                f'{self.outdir}/homer/factor-peaks.txt',
                f'{self.outdir}/homer/histone-regions.txt',
                f'{self.outdir}/macs2/broad-peaks.broadPeak',
                f'{self.outdir}/macs2/narrow-peaks.narrowPeak',
            ],
            genome_version='hg38'
        )

        annotated_files = [
            f'{self.outdir}/homer/factor-peaks-annotated.tsv',
            f'{self.outdir}/homer/histone-regions-annotated.tsv',
            f'{self.outdir}/macs2/broad-peaks-annotated.tsv',
            f'{self.outdir}/macs2/narrow-peaks-annotated.tsv',
        ]
        for f in annotated_files:
            self.assertTrue(exists(f))

    def __move_test_files_to_outdir(self):
        for d in ['homer', 'macs2']:
            src = f'{self.indir}/{d}'
            dst = f'{self.outdir}/{d}'
            if exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
