rule cleanup_single:
    input:
        check_file_raw="results/raw_reads/single_end/{single_reads}/{single_reads}_check_file_raw.txt",
        check_file_trim="results/trimmed_reads/single_end/{single_reads}_trimmed.txt",
        check_file_fasta="results/trimmed_fasta/single_end/{single_reads}_check_file_fastq2fasta.txt",
        check_file_diamond="results/diamond_bacteriocins/single_end/{single_reads}_check_file_diamond.txt",
    output:
        check_file_cleaned_raw="results/raw_reads/single_end/{single_reads}/{single_reads}_check_file_raw_cleaned.txt",
        check_file_cleaned_trim="results/trimmed_reads/single_end/{single_reads}_check_file_trimmed_cleaned.txt",
        check_file_cleaned_fasta="results/trimmed_fasta/single_end/{single_reads}_check_file_fastq2fasta_cleaned.txt",
    params:
        check_final_file_raw1="results/raw_reads/single_end/{single_reads}/{single_reads}.fastq.gz",
        check_final_file_trim1="results/trimmed_reads/single_end/{single_reads}.trimmed.fastq",
        check_final_file_fasta1="results/trimmed_fasta/single_end/{single_reads}.trimmed.fasta",
    shell:
        """
        # delete raw reads
        rm {params.check_final_file_raw1}
        touch {params.check_final_file_raw1}
        touch {output.check_file_cleaned_raw}

        # delete trimmed reads
        rm {params.check_final_file_trim1}
        touch {params.check_final_file_trim1}
        touch {output.check_file_cleaned_trim}

        # delete fasta file with reads
        rm {params.check_final_file_fasta1}
        touch {params.check_final_file_fasta1}
        touch {output.check_file_cleaned_fasta}
        """

rule cleanup_paired:
    input:
        check_file_raw="results/raw_reads/paired_end/{paired_reads}/{paired_reads}_check_file_raw.txt",
        check_file_trim="results/trimmed_reads/paired_end/{paired_reads}_trimmed.txt",
        check_file_fasta="results/trimmed_fasta/paired_end/{paired_reads}_check_file_fastq2fasta.txt",
        check_file_diamond="results/diamond_bacteriocins/paired_end/{paired_reads}_check_file_diamond.txt",
    output:
        check_file_cleaned_raw="results/raw_reads/paired_end/{paired_reads}/{paired_reads}_check_file_raw_cleaned.txt",
        check_file_cleaned_trim="results/trimmed_reads/paired_end/{paired_reads}_check_file_trimmed_cleaned.txt",
        check_file_cleaned_fasta="results/trimmed_fasta/paired_end/{paired_reads}_check_file_fastq2fasta_cleaned.txt",
    params:
        check_final_file_raw1="results/raw_reads/paired_end/{paired_reads}/{paired_reads}_1.fastq.gz",
        check_final_file_raw2="results/raw_reads/paired_end/{paired_reads}/{paired_reads}_2.fastq.gz",
        check_final_file_trimM="results/trimmed_reads/paired_end/{paired_reads}_merged.trimmed.fastq",
        check_final_file_fasta1="results/trimmed_fasta/paired_end/{paired_reads}_merged.trimmed.fasta",
    shell:
        """
        # delete raw reads
        rm {params.check_final_file_raw1}
        touch {params.check_final_file_raw1}
        rm {params.check_final_file_raw2}
        touch {params.check_final_file_raw2}
        touch {output.check_file_cleaned_raw}


        # delete trimmed reads
        rm {params.check_final_file_trimM}
        touch {params.check_final_file_trimM}
        touch {output.check_file_cleaned_trim}

        # delete fasta file with reads
        rm {params.check_final_file_fasta1}
        touch {params.check_final_file_fasta1}
        touch {output.check_file_cleaned_fasta}
        """

