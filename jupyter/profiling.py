#%%
import pandas as pd
data_path = "/Users/luanluan/Documents/Data/dw_airflow/data/radar/2020/Pro-Raw(1-8)T7-2020/01/"
read_file = pd.read_csv(data_path + "NHB200701001009.RAWXPS9.csv")
read_file.head(5)

#%%
read_file.describe()

#%%
import pandas as pd
from pandas_profiling import ProfileReport

profile = ProfileReport(
    read_file, title="Pandas Profiling Report for Nhabe Radar dataset"
)
profile.to_file("../data_to_web/NHB200701001009.RAWXPS9_profiling.html")