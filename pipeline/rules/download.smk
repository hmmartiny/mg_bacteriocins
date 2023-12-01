
rule download_single_end:
    output:
        "results/raw_reads/single_end/{single_reads}/{single_reads}.fastq.gz",
        check_file_raw="results/raw_reads/single_end/{single_reads}/{single_reads}_check_file_raw.txt"
    params:
        outdir="results/raw_reads/single_end/",
        type="fastq"
    benchmark:
        "results/raw_reads/single_end/{single_reads}.bench"
    log:
        "results/raw_reads/single_end/{single_reads}.log"
    threads: 8
    shell:
        """
            mkdir -p {params.outdir}{wildcards.single_reads}
            fastq-dl --accession {wildcards.single_reads} --outdir {params.outdir}{wildcards.single_reads} --silent --max-attempts 2 --cpus {threads} --force > {log}
            touch {output.check_file_raw}
        """

rule download_paired_end:
    output:
        "results/raw_reads/paired_end/{paired_reads}/{paired_reads}_1.fastq.gz",
        "results/raw_reads/paired_end/{paired_reads}/{paired_reads}_2.fastq.gz",
        check_file_raw="results/raw_reads/paired_end/{paired_reads}/{paired_reads}_check_file_raw.txt"
    params:
        outdir="results/raw_reads/paired_end/",
        type="fastq",
    benchmark:
        "results/raw_reads/paired_end/{paired_reads}.bench"
    log:
        "results/raw_reads/paired_end/{paired_reads}.log"
    threads: 8
    shell:
        """
            mkdir -p {params.outdir}{wildcards.paired_reads}
            fastq-dl --accession {wildcards.paired_reads} --outdir {params.outdir}{wildcards.paired_reads} --silent --max-attempts 2 --cpus {threads} --force > {log}
            touch {output.check_file_raw}
        """

