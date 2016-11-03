#!/usr/bin/env python3
import pandas as pd
import sys

infile = sys.argv[1]
outfile = "num." + infile
df = pd.read_table(infile, sep=" ", header=None, dtype=pd.np.object)
df[0] = df[0].map(lambda x: x.split(".")[1])
df.columns = ["batch", "perm"]
df['perm'] = df["perm"].map(lambda x: x.split(".")[-1].rstrip(")"))
print(df)
df.to_csv(outfile, sep="\t", index=False)

