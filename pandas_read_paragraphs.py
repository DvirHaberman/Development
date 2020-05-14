import pandas as pd
import bisect

df = pd.read_csv('paragraphs2.txt', sep="\r\n\r\n")

print(df)