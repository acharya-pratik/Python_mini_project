import numpy as np
import pandas as pd

class DataCleaner:
    def __init__(self, numeric_fill='mean', categorical_fill='mode',
                 date_columns=None, z_thresh=3):
        self.numeric_fill = numeric_fill
        self.categorical_fill = categorical_fill
        self.date_columns = date_columns or []
        self.z_thresh = z_thresh

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        original_shape = df.shape

        df = df.drop_duplicates()
        df = self.handle_missing(df)
        df = self.convert_dates(df)
        df = self.remove_outliers(df)
        # summary kta ho
        print("Cleaning Report:\n")
        print(f"Original shape : {original_shape}")
        print(f"Cleaned shape  : {df.shape}")
        print(f"Rows removed   : {original_shape[0] - df.shape[0]}")
        print(f"Remaining nulls: {df.isnull().sum().sum()}")
        return df

    def handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        # Strip whitespace from strings 
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()

        for col in df.select_dtypes(include=np.number).columns:
            if self.numeric_fill == 'mean':
                df[col] = df[col].fillna(df[col].mean())
            elif self.numeric_fill == 'median':
                df[col] = df[col].fillna(df[col].median())  # fixed typo
            elif isinstance(self.numeric_fill, (int, float)):
                df[col] = df[col].fillna(self.numeric_fill)

        for col in df.select_dtypes(include='object').columns:
            if self.categorical_fill == 'mode':
                df[col] = df[col].fillna(df[col].mode()[0])
            elif isinstance(self.categorical_fill, str):
                df[col] = df[col].fillna(self.categorical_fill)

        return df

    def convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in self.date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')  # fixed typo
        return df

    def remove_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_cols = df.select_dtypes(include=np.number).columns
        mask = pd.Series([True] * len(df), index=df.index)
        for col in numeric_cols:
            std = df[col].std()
            if std == 0:
                continue
            z_score = (df[col] - df[col].mean()) / std
            mask = mask & (z_score.abs() <= self.z_thresh)
        return df[mask]

# if __name__ == "__main__":
#     df = pd.read_csv("sample_data.csv")
#     cleaner = DataCleaner(
#         numeric_fill='mean',
#         categorical_fill='mode',
#         date_columns=['Date of Admission', 'Discharge Date'],
#         z_thresh=3
#     )
#     clean_df = cleaner.clean(df)
#     clean_df.to_csv('cleaned_data.csv', index=False)
#     print(clean_df.head())