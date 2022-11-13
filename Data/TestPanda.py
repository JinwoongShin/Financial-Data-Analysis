import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

a = {'A' : [1, 2, 3, 4, 5], 'B' : [10, 20, 30, 40, 50], 'C' : [100, 200, 300, 400, 500]}
df = pd.DataFrame(a, index = ['가', '나', '다', '라', '마'])
print(df)