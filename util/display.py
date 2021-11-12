def display_dict(dct):
    for i in dct.keys():
        print(i.title() + ": ", dct[i])

def display_pandas_rbr(df):
    for index, row in df.iterrows():
        for col in df.columns:
            print(col.title() + ": ", row[col])
        print("\n")