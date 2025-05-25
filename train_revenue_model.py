
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# Load the dataset
df = pd.read_csv("supply_chain_data.csv")

# Drop columns that are not useful for prediction
df_clean = df.drop(columns=["SKU", "Revenue generated"])

# Target variable
y = df["Revenue generated"]

categorical_cols = df_clean.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = df_clean.select_dtypes(include=["int64", "float64"]).columns.tolist()

# Preprocessing for numerical and categorical data
numerical_transformer = SimpleImputer(strategy="mean")
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_cols),
        ("cat", categorical_transformer, categorical_cols)
    ])

model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(df_clean, y, test_size=0.2, random_state=42)

model.fit(X_train, y_train)

joblib.dump(model, "revenue_prediction_model.joblib")
