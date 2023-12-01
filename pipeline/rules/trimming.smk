
rule trim_single_end_reads:
    input:
        ancient("results/raw_reads/single_end/{single_reads}/{single_reads}.fastq.gz")
    output:
        o="results/trimmed_reads/single_end/{single_reads}.trimmed.fastq",
        check_file_trim="results/trimmed_reads/single_end/{single_reads}_trimmed.txt"
    benchmark:
        "results/trimmed_reads/single_end/{single_reads}.bench",
    log:
        "results/trimmed_reads/single_end/{single_reads}.log",
    params:
        overlap_diff_limit="1",
        average_qual="20",
        length_required="50",
        cut_tail="--cut_tail",
        h="results/trimmed_reads/single_end/{single_reads}.html",
        j="results/trimmed_reads/single_end/{single_reads}.json"
    threads: 16
    shell:
        """
        timeout 2h fastp -i {input} -o {output.o} --overlap_diff_limit {params.overlap_diff_limit} --average_qual {params.average_qual} --length_required {params.length_required} {params.cut_tail} -h {params.h} -j {params.j} -w {threads} > {log}
        touch {output.check_file_trim}
        """

rule trim_paired_end_reads:
    input:
        in1=ancient("results/raw_reads/paired_end/{paired_reads}/{paired_reads}_1.fastq.gz"),
        in2=ancient("results/raw_reads/paired_end/{paired_reads}/{paired_reads}_2.fastq.gz")
    output:
        out_merge="results/trimmed_reads/paired_end/{paired_reads}_merged.trimmed.fastq",
        check_file_trim="results/trimmed_reads/paired_end/{paired_reads}_trimmed.txt"
    benchmark:
        "results/trimmed_reads/paired_end/{paired_reads}.bench",
    log:
        "results/trimmed_reads/paired_end/{paired_reads}.log",
    params:
        overlap_diff_limit="1",
        average_qual="20",
        length_required="50",
        cut_tail="--cut_tail",
        h="results/trimmed_reads/paired_end/{paired_reads}.html",
        j="results/trimmed_reads/paired_end/{paired_reads}.json"
    threads: 16
    shell:
        """
        timeout 2h fastp -i {input.in1} -I {input.in2} --merge --merged_out {output.out_merge} --include_unmerged --overlap_diff_limit {params.overlap_diff_limit} --average_qual {params.average_qual} --length_required {params.length_required} {params.cut_tail} -h {params.h} -j {params.j} -w {threads} > {log}

        touch {output.check_file_trim}
        """
