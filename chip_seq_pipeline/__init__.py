import os
from .template import Settings
from .tools import get_temp_path
from .chip_seq_pipeline import ChipSeqPipeline


def main(
        ref_fa: str,
        treatment_fq1: str,
        treatment_fq2: str,
        control_fq1: str,
        control_fq2: str,

        base_quality_cutoff: int,
        min_read_length: int,

        read_aligner: str,
        bowtie2_mode: str,
        discard_bam: bool,

        skip_mark_duplicates: bool,

        macs_effective_genome_size: str,
        macs_fdr: float,

        genome_version: str,
        skip_motif_finding: bool,
        motif_finding_fragment_size: int,

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
        treatment_fq1=treatment_fq1,
        treatment_fq2=treatment_fq2,
        control_fq1=None if control_fq1.lower() == 'none' else control_fq1,
        control_fq2=None if control_fq2.lower() == 'none' else control_fq2,

        base_quality_cutoff=base_quality_cutoff,
        min_read_length=min_read_length,

        read_aligner=read_aligner,
        bowtie2_mode=bowtie2_mode,
        discard_bam=discard_bam,

        skip_mark_duplicates=skip_mark_duplicates,

        macs_effective_genome_size=macs_effective_genome_size,
        macs_fdr=macs_fdr,

        genome_version=genome_version,
        skip_motif_finding=skip_motif_finding,
        motif_finding_fragment_size=motif_finding_fragment_size)
