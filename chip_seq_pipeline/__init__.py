import os
from .template import Settings
from .tools import get_temp_path
from .chip_seq_pipeline import ChipSeqPipeline


def main(
        ref_fa: str,
        fq1: str,
        fq2: str,
        gtf: str,

        base_quality_cutoff: int,
        min_read_length: int,
        max_read_length: int,

        read_aligner: str,
        bowtie2_mode: str,
        discard_bam: bool,

        outdir: str,
        threads: int,
        debug: bool):

    settings = Settings(
        workdir=get_temp_path(prefix='./chip_seq_workdir_'),
        outdir=outdir,
        threads=threads,
        debug=debug,
        mock=False)

    for d in [settings.workdir, settings.outdir]:
        os.makedirs(d, exist_ok=True)

    ChipSeqPipeline(settings=settings).main(
        ref_fa=ref_fa,
        treatment_fq1=fq1,
        treatment_fq2=fq2,
        gtf=gtf,

        base_quality_cutoff=base_quality_cutoff,
        min_read_length=min_read_length,
        max_read_length=max_read_length,

        read_aligner=read_aligner,
        bowtie2_mode=bowtie2_mode,
        discard_bam=discard_bam)
