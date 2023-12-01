import argparse
import pandas as pd
import os
import json
import multiprocessing
import subprocess

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-b', '--batch_file',
        type=str,
        required=True,
        help='run_accessions to download',
        dest='batch_file'
    )

    parser.add_argument(
        '-df', '--datafile',
        type=str,
        required=True,
        help='File with fastq links and md5sums',
        dest='data'
    )

    parser.add_argument(
        '-d', '--dest',
        type=str,
        required=True,
        help='Destionation to store downloaded fastq files in',
        dest='dest'
    )

    parser.add_argument(
        '-o', '--outfile',
        type=str,
        required=True,
        help='File with new json files listed',
        dest='outputfile'
    )

    parser.add_argument(
        '-bs', '--batch_size',
        type=int,
        default=100,
        help='how many to download at once',
        dest='batch_size'
    )

    parser.add_argument(
        '-np', '--num_proc',
        type=int,
        default=10,
        help='number of multiprocessing ',
        dest='np'
    )

    return parser.parse_args()

def get_ftp_file(ftp_url, dest):
    filename = urlparse.unquote(ftp_url.split('/')[-1])
    dest_file = os.path.join(dest, filename)
    urlrequest.urlretrieve(ftp_url, dest_file)

def make_ascp(ascplink, dest):
    os.makedirs(dest, exist_ok=True)
    #wget_cmd = f"wget -c -N --quiet --directory-prefix={dest} --tries=3 --waitretry=5 ftp://{ftp}"
    ascp_cmd = f"ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@{ascplink} {dest}"
    return ascp_cmd

def run(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print(f"Failed: {cmd}\nstderr: {p.stderr.decode()}\nstdout: {p.stdout.decode()}")   
    else:
        print(f"Finished {cmd}")

def run_ascps(cmds, np=10):
    p = multiprocessing.Pool(np)
    p.map(run, cmds)


if __name__ == "__main__":
    args = parse_args()
    
    df = pd.read_csv(args.data, sep='\t')
    os.makedirs(args.dest, exist_ok=True)

    o = open(args.outputfile, 'w')

    with open(args.batch_file, 'r') as f:
        fullBatch = json.load(f)

    print(f"Loaded batch {os.path.basename(args.batch_file)} consisting of {len(fullBatch)} run_accessions")
    print(f".. splitting it into chunks of size {args.batch_size}")
    run_ids = list(fullBatch.keys())

    n = 1
    for i in range(0, len(run_ids), args.batch_size):
        sub_batch = run_ids[i:i+args.batch_size]
        sub_dict = {r: fullBatch[r] for r in sub_batch}
        sub_df = df.loc[df.run_accession.isin(sub_batch), ].copy()
        sub_df['fastq_aspera'] = sub_df.fastq_aspera.str.split(';')
        sub_df['fastq_md5'] = sub_df.fastq_md5.str.split(';')
        sub_ftps = sub_df[['run_accession', 'fastq_aspera']].explode('fastq_aspera')
        sub_ftps['read_type'] = sub_ftps['run_accession'].map(sub_dict).apply(lambda x: x['library_layout']).str.lower()
        sub_md5s = sub_df[['run_accession', 'fastq_md5']].explode('fastq_md5')

        ascp_cmds = sub_ftps.apply(lambda x: make_ascp(ascplink=x['fastq_aspera'], dest=os.path.join(args.dest, x['read_type']+'_end', x['run_accession'])), axis=1).values.tolist()
        
        #run_ascps(cmds=ascp_cmds, np=args.np)
        with open(args.batch_file.replace('.json', f".{n}.cmds"), 'w') as of:
            print("\n".join(ascp_cmds), file=of)

        # write subset json to file
        sub_json = args.batch_file.replace('.json', f".{n}.json")
        with open(sub_json, 'w') as f:
            json.dump(sub_dict, f)
        print(os.path.realpath(sub_json), file=o)
        n += 1

    o.close()
