import subprocess
import pandas as pd
from io import StringIO
import pycoda
import warnings

def query_db(query):
    p = subprocess.run(f"mysql -e \"{query}\"", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return pd.read_csv(StringIO(p.stdout.decode()), sep='\t')

def extract_group(sseq_overgroup, bacteriocinCounts2, qpsLABDF):
    Mat = bacteriocinCounts2.query(f"group_name == '{sseq_overgroup}'").pivot_table(
        index=['run_accession', 'biome', 'category', 'country'], 
        columns='sseqid', 
        values='adj_count', 
        fill_value=0
    )
    with warnings.catch_warnings(action='ignore'):
        ZRMat = Mat.coda.zero_replacement()
        ZRMat.index = Mat.index.get_level_values(level=0)

    qpsLabSum = qpsLABDF.groupby('run_accession').agg({'fragmentCountAln': 'sum'}).rename(columns={'fragmentCountAln': 'QPS-LAB'})
    Mat3 = ZRMat.merge(qpsLabSum / 1e6, left_index=True, right_index=True)
    
    with warnings.catch_warnings(action='ignore'):
        ALRMat = Mat3.coda.alr()
        CLRMat = ZRMat.coda.clr() 
    
    return Mat, ZRMat, ALRMat, CLRMat