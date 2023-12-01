
rule fastq2fasta_single:
    input:
        ancient("results/trimmed_reads/single_end/{single_reads}.trimmed.fastq")
    output:
        o="results/trimmed_fasta/single_end/{single_reads}.trimmed.fasta",
        check_file_fasta="results/trimmed_fasta/single_end/{single_reads}_check_file_fastq2fasta.txt"
    benchmark:
        "results/trimmed_fasta/single_end/{single_reads}.bench"
    log:
        "results/trimmed_fasta/single_end/{single_reads}.log"
    threads: 4
    shell:
        """
        seqkit fq2fa -j {threads} {input} -o {output.o} > {log}

        touch {output.check_file_fasta}
        """
rule fastq2fasta_paired:
    input:
        ancient("results/trimmed_reads/paired_end/{paired_reads}_merged.trimmed.fastq")
    output:
        o="results/trimmed_fasta/paired_end/{paired_reads}_merged.trimmed.fasta",
        check_file_fasta="results/trimmed_fasta/paired_end/{paired_reads}_check_file_fastq2fasta.txt"
    benchmark:
        "results/trimmed_fasta/paired_end/{paired_reads}.bench",
    log:
        "results/trimmed_fasta/paired_end/{paired_reads}.log",
    envmodules:
        "tools",
    params:
        outdir="results/trimmed_fasta/paired_end/"
    threads: 4
    shell:
        """
        seqkit fq2fa -j {threads} {input} -o {output.o} > {log}

        touch {output.check_file_fasta}
        """

rule diamond_bacteriocins_single:
    input:
        ancient("results/trimmed_fasta/single_end/{single_reads}.trimmed.fasta")
    output:
        o="results/diamond_bacteriocins/single_end/{single_reads}.tsv",
        check_file_diamond="results/diamond_bacteriocins/single_end/{single_reads}_check_file_diamond.txt"
    benchmark:
        "results/diamond_bacteriocins/single_end/{single_reads}.bench"
    log:
        "results/diamond_bacteriocins/single_end/{single_reads}.log"
    params:
        db="prerequisites/bacteriocins/bacteriocins"
    threads: 32
    shell:
        """
        diamond blastx --db {params.db} --out {output.o} --outfmt 6 --id 90 --evalue 1e-5 --query {input} --threads {threads} --quiet --fast > {log}

        touch {output.check_file_diamond}
        """
rule diamond_bacteriocins_paired:
    input:
        ancient("results/trimmed_fasta/paired_end/{paired_reads}_merged.trimmed.fasta"),
    output:
        o="results/diamond_bacteriocins/paired_end/{paired_reads}.tsv",
        check_file_diamond="results/diamond_bacteriocins/paired_end/{paired_reads}_check_file_diamond.txt"
    benchmark:
        "results/diamond_bacteriocins/paired_end/{paired_reads}.bench"
    log:
        "results/diamond_bacteriocins/paired_end/{paired_reads}.log"
    params:
        db="prerequisites/bacteriocins/bacteriocins"
    threads: 32
    shell:
        """
        diamond blastx --db {params.db} --out {output.o} --outfmt 6 --id 90 --evalue 1e-5 --query {input} --threads {threads} --quiet --fast > {log}
        touch {output.check_file_diamond}
        """
