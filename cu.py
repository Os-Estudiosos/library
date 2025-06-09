import pandas as pd

cu = [(1,2, "Alex"), (3,4, "Bob"), (5,6, "Charlie")]
df = pd.DataFrame(cu, columns=["x", "y", "name"])
df["junto"] = df["x"].astype(str) + df["y"].astype(str)
print(df)