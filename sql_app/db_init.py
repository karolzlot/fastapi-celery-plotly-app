

def db_init():
    import pandas as pd

    from .database import engine

    columns_types={
    'DBN'                    : 'str', 
    'School_Name'            : 'str', 
    'Category'               : 'str', 
    'Year'                   : 'str', 
    'Total_Enrollment'       : 'Int64', 
    'Grade_K'                : 'Int64', 
    'Grade_1'                : 'Int64', 
    'Grade_2'                : 'Int64', 
    'Grade_3'                : 'Int64', 
    'Grade_4'                : 'Int64', 
    'Grade_5'                : 'Int64', 
    'Grade_6'                : 'Int64', 
    'Grade_7'                : 'Int64', 
    'Grade_8'                : 'Int64', 
    'Female'                 : 'Int64', 
    'Female_pct'             : 'float', 
    'Male'                   : 'Int64', 
    'Male_pct'               : 'float', 
    'Asian'                  : 'Int64', 
    'Asian_pct'              : 'float', 
    'Black'                  : 'Int64', 
    'Black_pct'              : 'float', 
    'Hispanic'               : 'Int64', 
    'Hispanic_pct'           : 'float', 
    'Other'                  : 'Int64', 
    'Other_pct'              : 'float', 
    'White'                  : 'Int64', 
    'White_pct'              : 'float', 
    'ELL_Spanish'            : 'Int64', 
    'ELL_Spanish_pct'        : 'float', 
    'ELL_Chinese'            : 'Int64', 
    'ELL_Chinese_pct'        : 'float', 
    'ELL_Bengali'            : 'Int64', 
    'ELL_Bengali_pct'        : 'float', 
    'ELL_Arabic'             : 'Int64', 
    'ELL_Arabic_pct'         : 'float', 
    'ELL_Haitian_Creole'     : 'Int64', 
    'ELL_Haitian_Creole_pct' : 'float', 
    'ELL_French'             : 'Int64', 
    'ELL_French_pct'         : 'float', 
    'ELL_Russian'            : 'Int64', 
    'ELL_Russian_pct'        : 'float', 
    'ELL_Korean'             : 'Int64', 
    'ELL_Korean_pct'         : 'float', 
    'ELL_Urdu'               : 'Int64', 
    'ELL_Urdu_pct'           : 'float', 
    'ELL_Other'              : 'Int64', 
    'ELL_Other_pct'          : 'float', 
    'ELA_Test_Takers'        : 'Int64', 
    'ELA_Level_1'            : 'Int64', 
    'ELA_Level_1_pct'        : 'float', 
    'ELA_Level_2'            : 'Int64', 
    'ELA_Level_2_pct'        : 'float', 
    'ELA_Level_3'            : 'Int64', 
    'ELA_Level_3_pct'        : 'float', 
    'ELA_Level_4'            : 'Int64', 
    'ELA_Level_4_pct'        : 'float', 
    'ELA_L3_and_L4'          : 'Int64', 
    'ELA_L3_and_L4_pct'      : 'float', 
    'MATH_Test_Takers'       : 'Int64', 
    'MATH_Level_1'           : 'Int64', 
    'MATH_Level_1_pct'       : 'float', 
    'MATH_Level_2'           : 'Int64', 
    'MATH_Level_2_pct'       : 'float', 
    'MATH_Level_3'           : 'Int64', 
    'MATH_Level_3_pct'       : 'float', 
    'MATH_Level_4'           : 'Int64', 
    'MATH_Level_4_pct'       : 'float', 
    'MATH_L3_and_L4'         : 'Int64', 
    'MATH_L3_and_L4_pct'     : 'float', 
    }

    columns_names=columns_types.keys()

    columns_to_keep=[
    'DBN', 
    'Category', 
    'Total_Enrollment', 
    'Female_pct', 
    'Male_pct', 
    'Asian_pct', 
    'Black_pct', 
    'Hispanic_pct', 
    'Other_pct', 
    'White_pct', 
    'ELA_Level_1', 
    'ELA_Level_2', 
    'ELA_L3_and_L4', 
    'MATH_Level_1', 
    'MATH_Level_2', 
    'MATH_L3_and_L4', 
    ]

    df = pd.read_csv('https://data.cityofnewyork.us/api/views/7yc5-fec2/rows.csv?accessType=DOWNLOAD',header=0,dtype=columns_types,names=columns_names,na_values=['s','No Data',' '], usecols=columns_to_keep)
    df["District"] = df['DBN'].str[0:2].astype(int)

    df = df.dropna(subset = ['Female_pct','Male_pct','Total_Enrollment']) # cleaning rows with incomplete data
    
    df.drop('Total_Enrollment', axis=1, inplace=True) # column not needed anymore

    df.update(df[['Asian_pct','Black_pct','Hispanic_pct','Other_pct','White_pct','ELA_Level_1','ELA_Level_2','ELA_L3_and_L4','MATH_Level_1','MATH_Level_2','MATH_L3_and_L4']].fillna(0))

    df.to_sql(name='schools_stats_entries', con=engine, if_exists = 'append', index=False)

