#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

df = pd.read_csv("../data/medicine_data.csv")


# In[3]:


df.columns.tolist()


# In[4]:


df.head()


# In[5]:


df.columns


# In[6]:


df.info()


# In[7]:


df.isnull().sum()


# In[8]:


df["price_inr"].describe()


# In[9]:


df["active_ingredients"].head(10)


# In[10]:


df["manufacturer"].head(10)


# In[11]:


df.isnull().sum().sort_values(ascending=False)


# In[12]:


# requiredColumns = [
#     "brand_name", 
#     "manufacturer", 
#     "price_inr",
#     "dosage_form", 
#     "pack_size",
#     "primary_ingredient",
#     "primary_strength",
#     "active_ingredients", 
#     "therapeutic_class"
# ]

# df = df[requiredColumns]


# In[13]:


df.head()


# In[14]:


df["active_ingredients"].head(20)


# In[15]:


df["primary_ingredient"].head(20)


# In[16]:


import ast

def clean_composition(text):
    if pd.isna(text):
        return ""

    try:
        ingredients = ast.literal_eval(text)

        result = []

        for ing in ingredients:
            name = str(ing.get("name") or "").strip().lower()
            strength = str(ing.get("strength") or "unknown").strip().lower()

            if not name:
                continue

            result.append(f"{name}_{strength}")

        result.sort()

        return " ".join(result)

    except (ValueError, SyntaxError, TypeError):
        return ""


# In[17]:


df["cleaned_composition"] = (
    df["active_ingredients"].apply(clean_composition)
)


# In[18]:


(df["cleaned_composition"] == "").sum()


# In[19]:


print("Empty compositions:", (df["cleaned_composition"] == "").sum())
print("Missing compositions:", df["cleaned_composition"].isna().sum())


# In[20]:


df = df[df["price_inr"] > 0].copy()


# In[21]:


len(df)


# In[22]:


df[
    [
        "active_ingredients",
        "cleaned_composition"
    ]
].head()


# In[23]:


df["cleaned_composition"].value_counts().head(10)


# In[24]:


def find_alternatives(medicineName):

    medicine = df[
        df["brand_name"].str.lower() == medicineName.lower()
    ]

    if medicine.empty:
        print("Medicine not found.")
        return None

    composition = medicine.iloc[0]["cleaned_composition"]

    alternatives = df[
        df["cleaned_composition"] == composition
    ]

    alternatives = alternatives.sort_values(by="price_inr")

    return alternatives[
        [
            "brand_name",
            "manufacturer",
            "price_inr"
        ]
    ]


# In[25]:


df["brand_name"].head(20)


# In[26]:


find_alternatives("Azee 500 Tablet")


# In[27]:


df["price_inr"].describe()


# In[28]:


(df["price_inr"] <= 0).sum()


# In[29]:


(df["cleaned_composition"] == "").sum()


# In[30]:


df["cleaned_composition"].isna().sum()


# In[31]:


print("Empty compositions:", (df["cleaned_composition"] == "").sum())
print("Missing compositions:", df["cleaned_composition"].isna().sum())


# In[32]:


df = df[df["price_inr"] > 0].copy()


# In[33]:


df["price_inr"].quantile(
    [0.90, 0.95, 0.99, 0.995, 0.999]
)


# In[34]:


df[
    [
        "brand_name",
        "manufacturer",
        "price_inr",
        "dosage_form",
        "primary_ingredient"
    ]
].sort_values(
    "price_inr",
    ascending=False
).head(20)


# In[35]:


df.columns


# In[36]:


df["price_inr"].sort_values(
    ascending=False
).head(20)


# In[37]:


df["dosage_form"].value_counts().head(15)


# In[38]:


df["therapeutic_class"].value_counts().head(15)


# In[39]:


df["pack_size"].value_counts().head(20)


# In[40]:


df["pack_size"].describe()


# In[41]:


df["cleaned_composition"].nunique()


# ## Price Distribution
# 
# Medicine prices are highly right skewed, most of the medicines are priced normally but some are egregiously priced going upto something like Rs. 450k
# I mean it's no 'murican healthcare but still that's clearly price gouging for life saving medicines
# 
# Anyways back to the project
# 

# In[42]:


import numpy as np


# In[43]:


import matplotlib.pyplot as plt

plt.figure (figsize=(10, 5))

plt.hist(df["price_inr"], bins=100)

plt.title("Distribution of medicine prices")
plt.xlabel("Price (INR)")
plt.ylabel("Number of medicines")

plt.show()


# In[44]:


import matplotlib.pyplot as plt

plt.figure (figsize=(10, 5))

plt.hist(df["price_inr"], bins=100)

plt.xscale("log")

plt.title("Distribution of medicine prices (x -> log scale)")
plt.xlabel("Price (INR)")
plt.ylabel("Number of medicines")

plt.show()


# In[45]:


import matplotlib.pyplot as plt

plt.figure (figsize=(10, 5))

plt.hist(np.log1p(df["price_inr"]), bins=100)

plt.title("Distribution of medicine prices (x -> log scale)")
plt.xlabel("log(1 + Price (INR))")
plt.ylabel("Number of medicines")

plt.show()


# In[46]:


composition_stats = (
    df.groupby("cleaned_composition")
    .agg(
        median_price=("price_inr", "median"),
        medicine_count=("price_inr", "count")
    )
)

composition_stats = composition_stats[
    composition_stats["medicine_count"] >= 50
]

top_compositions = (
    composition_stats
    .sort_values("median_price", ascending=False)
    .head(15)
)

plt.figure(figsize=(12,7))

top_compositions["median_price"].sort_values().plot(
    kind="barh"
)

plt.title("Top 15 composition groups by Median Price")
plt.xlabel("Median Price (INR)")
plt.ylabel("Compositions")

plt.show()


# In[47]:


manufacturer_stats = (
    df.groupby("manufacturer")
    .agg(
        median_price=("price_inr", "median"),
        medicine_count=("price_inr", "count")
    )
)

manufacturer_stats = manufacturer_stats[
    manufacturer_stats["medicine_count"] >= 50
]

top_manufacturers = (
    manufacturer_stats
    .sort_values("median_price", ascending=False)
    .head(15)
)

plt.figure(figsize=(12,7))

top_manufacturers["median_price"].sort_values().plot(
    kind="barh"
)

plt.title("Top 15 manufacturers by Median Price")
plt.xlabel("Median Price (INR)")
plt.ylabel("Manufacturer")

plt.show()


# In[48]:


pack_stats = (
    df.groupby("pack_size")
    .agg(
        median_price=("price_inr", "median"),
        medicine_count=("price_inr", "count")
    )
)

pack_stats = pack_stats[
    (pack_stats["medicine_count"] >= 50) &
    (pack_stats.index <= 100)
]

plt.figure(figsize=(10, 5))

plt.scatter(
    pack_stats.index,
    pack_stats["median_price"]
)

plt.title("Pack Size vs Median Medicine Price")
plt.xlabel("Pack Size")
plt.ylabel("Median Price (INR)")

plt.show()


# In[49]:


pack_stats.sort_values(
    "median_price",
    ascending=False
).head(10)


# In[50]:


df[df["pack_size"] == 28].sort_values(
    "price_inr",
    ascending=False
).head(20)


# In[51]:


highest_pack = pack_stats["median_price"].idxmax()

print("Pack size:", highest_pack)
print("Median price:", pack_stats.loc[highest_pack, "median_price"])
print("Medicine count:", pack_stats.loc[highest_pack, "medicine_count"])


# In[52]:


features = [
    "dosage_form",
    "pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class",
    "num_active_ingredients"
]

target = "price_inr"

X = df[features].copy()
y = df[target].copy()


# In[53]:


df.columns.tolist()


# In[54]:


X.dtypes


# In[55]:


X.isnull().sum()


# In[56]:


from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


numeric_features = [
    "pack_size",
    "num_active_ingredients"
]

categorical_features = [
    "dosage_form",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class"
]


numeric_transformer = SimpleImputer(
    strategy="median"
)


categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(
        strategy="constant",
        fill_value="Unknown"
    )),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessor = ColumnTransformer([
    (
        "numeric",
        numeric_transformer,
        numeric_features
    ),
    (
        "categorical",
        categorical_transformer,
        categorical_features
    )
])


# In[57]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])


# In[58]:


model.fit(X_train, y_train)


# In[59]:


y_pred = model.predict(X_test)

comparison = pd.DataFrame(
    {
        "actual": y_test.values,
        "predicted":y_pred
    }
)

comparison.head(10)


# In[60]:


from sklearn.metrics import mean_absolute_error

mae = mean_absolute_error(y_test, y_pred)

print(f"MAE: ₹{mae:.2f}")


# In[61]:


from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)

print(f"R²: {r2:.4f}")


# In[62]:


plt.figure(figsize=(8,8))

plt.scatter(
    y_test,
    y_pred,
    alpha=0.2
)

plt.title("Actual vs Predicted Medicine Prices")
plt.xlabel("Actual Price (INR)")
plt.ylabel("Predicted Price (INR)")

plt.show()


# In[63]:


plt.figure(figsize=(8,8))

plt.scatter(
    np.log1p(y_test),
    np.log1p(y_pred),
    alpha=0.2
)

plt.title("Actual vs Predicted Medicine Prices (log Scale)")
plt.xlabel("log(1 + Actual Price)")
plt.ylabel("log(1 + Predicted Price)")

plt.show()


# In[64]:


comparison["absolute_error"] = (
    comparison["actual"] - comparison["predicted"]
).abs()

comparison.sort_values(
    "absolute_error",
    ascending=False
).head(20)

error_analysis = X_test.copy()

error_analysis["actual_price"] = y_test
error_analysis["predicted_price"] = y_pred

error_analysis["absolute_error"] = (
    error_analysis["actual_price"] - error_analysis["predicted_price"]
).abs()

error_analysis.sort_values(
    "absolute_error",
    ascending=False
).head(20)


# In[65]:


y_pred = model.predict(X_test)

from sklearn.metrics import mean_absolute_error,r2_score

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: ₹{mae:.2f}")
print(f"R²: {r2:.4f}")


# In[66]:


import numpy as np

y_train_log = np.log1p(y_train)

log_model = Pipeline([
    ("preprocessor", preprocessor),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])

log_model.fit(
    X_train,
    y_train_log
)


# In[67]:


y_pred_log = log_model.predict(X_test)

y_pred_log_price = np.expm1(y_pred_log)

log_mae = mean_absolute_error(
    y_test,
    y_pred_log_price
)

log_r2 = r2_score(
    y_test,
    y_pred_log_price
)

print(f"log model MAE: ₹{log_mae:.2f}")
print(f"log model R²: {log_r2:.4f}")


# ## log model is worse at predicting the prices

# In[68]:


comparison = pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred
})

comparison["absolute_error"] = (
    comparison["actual"] - comparison["predicted"]
).abs()

comparison.sort_values(
    "absolute_error",
    ascending=False
).head(20)


# In[69]:


error_analysis = X_test.copy()

error_analysis["actual_price"] = y_test
error_analysis["predicted_price"] = y_pred

error_analysis["absolute_error"] = (
    error_analysis["actual_price"]
    - error_analysis["predicted_price"]
).abs()

error_analysis.sort_values(
    "absolute_error",
    ascending=False
).head(20)


# In[70]:


features = [
    "manufacturer",
    "dosage_form",
    "pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class",
    "num_active_ingredients"
]

target = "price_inr"

X = df[features].copy()
y = df[target].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

manufacturer_counts = (
    X_train["manufacturer"].value_counts()
)

X_train_encoded = X_train.copy()
X_test_encoded = X_test.copy()

X_train_encoded["manufacturer_frequency"] = (
    X_train_encoded["manufacturer"]
    .map(manufacturer_counts)
    .fillna(0)
)

X_test_encoded["manufacturer_frequency"] = (
    X_test_encoded["manufacturer"]
    .map(manufacturer_counts)
    .fillna(0)
)

X_train_encoded = X_train_encoded.drop(
    columns=["manufacturer"]
)
X_test_encoded = X_test_encoded.drop(
    columns=["manufacturer"]
)

X_train_encoded = X_train_encoded.drop(
    columns=["brand_name"],
    errors="ignore"
)
X_test_encoded = X_test_encoded.drop(
    columns=["brand_name"],
    errors="ignore"
)

numeric_features = [
    "pack_size",
    "num_active_ingredients",
    "manufacturer_frequency"
]

categorical_features = [
    "dosage_form",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class"
]

numeric_transformer = SimpleImputer(
    strategy="median"
)

categorical_transformer = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="constant",
            fill_value="Unknown"
        )
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])

preprocessor_frequency = ColumnTransformer([
    (
        "numeric",
        numeric_transformer,
        numeric_features
    ),
    (
        "categorical",
        categorical_transformer,
        categorical_features
    )
])

model_frequency = Pipeline([
    ("preprocessor", preprocessor_frequency),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])


# In[71]:


df["manufacturer"].value_counts().head(20)


# In[72]:


# df[[
#     "brand_name",
#     "manufacturer"
# ]].nunique()

# Don't use brand_name because:
# brand_name      249394
# manufacturer      7647
# dtype: int64


# In[73]:


# X_train.shape

# (203175, 9)


# In[74]:


model_frequency.fit(
    X_train_encoded,
    y_train
)

y_pred_frequency = model_frequency.predict(X_test_encoded)


# In[75]:


mae_frequency = mean_absolute_error(
    y_test,
    y_pred_frequency
)

r2_frequency = r2_score(
    y_test,
    y_pred_frequency
)

print(f"MAE: ₹{mae_frequency:.2f}")
print(f"R²: {r2_frequency:.4f}")


# In[76]:


feature_names = model.named_steps["preprocessor"].get_feature_names_out()

importances = model.named_steps["regressor"].feature_importances_

feature_importance = (
    pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    })
    .sort_values(
        "importance",
        ascending=False
    )
)

feature_importance.head(20)


# In[77]:


from sklearn.metrics import mean_absolute_percentage_error

mape = mean_absolute_percentage_error(
    y_test,
    y_pred
)

print(f"MAPE: {mape * 100:.2f}%")


# In[78]:


evaluation = pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred
})

evaluation["absolute_error"] = (
    evaluation["actual"] - evaluation["predicted"]
).abs()

evaluation["price_range"] = pd.cut(
    evaluation["actual"],
    bins=[0, 100, 500, 2000, 10000, float("inf")],
    labels=[
        "₹0-100",
        "₹100-500",
        "₹500-2,000",
        "₹2,000-10,000",
        "₹10,000+"
    ]
)

range_performance = (
    evaluation
    .groupby("price_range", observed=True)
    .agg(
        medicine_count=("actual", "count"),
        mae=("absolute_error", "mean")
    )
)

range_performance


# In[79]:


from sklearn.ensemble import GradientBoostingRegressor

features = [
    "dosage_form",
    "pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class",
    "num_active_ingredients"
]

X = df[features].copy()
y = df["price_inr"].copy()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

numeric_features = [
    "pack_size",
    "num_active_ingredients"
]

categorical_features = [
    "dosage_form",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class"
]

numeric_transformer = SimpleImputer(
    strategy="median"
)

categorical_transformer = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="constant",
            fill_value="Unknown"
        )
    ),
    (
        "encoder",
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )
])

preprocessor_baseline = ColumnTransformer([
    (
        "numeric",
        numeric_transformer,
        numeric_features
    ),
    (
        "categorical",
        categorical_transformer,
        categorical_features
    )
])

gradient_model = Pipeline([
    (
        "preprocessor",
        preprocessor_baseline
    ),
    (
        "regressor",
        GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        )
    )
])


# In[80]:


gradient_model.fit(
    X_train,
    y_train
)

y_pred_gradient = gradient_model.predict(
    X_test
)


# In[81]:


mae_gradient = mean_absolute_error(
    y_test,
    y_pred_gradient
)

r2_gradient = r2_score(
    y_test,
    y_pred_gradient
)

print(f"Gradient Boosting MAE: ₹{mae_gradient:.2f}")
print(f"Gradient Boosting R²: {r2_gradient:.4f}")


# In[82]:


rf_tuned = Pipeline([
    (
        "preprocessor",
        preprocessor_baseline
    ),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=200,
            max_depth=25,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    )
])

rf_tuned.fit(
    X_train,
    y_train
)

y_pred_rf_tuned = rf_tuned.predict(
    X_test
)

mae_rf_tuned = mean_absolute_error(
    y_test,
    y_pred_rf_tuned
)

r2_rf_tuned = r2_score(
    y_test,
    y_pred_rf_tuned
)

print(f"MAE: ₹{mae_rf_tuned:.2f}")
print(f"R²: {r2_rf_tuned:.4f}")


# In[83]:


df["strength_value"] = (
    df["primary_strength"]
    .astype(str)
    .str.extract(r"(\d+(?:\.\d+)?)")[0]
    .astype(float)
)

df["log_pack_size"] = np.log1p(df["pack_size"])


# In[84]:


features_engineered = [
    "dosage_form",
    "pack_size",
    "log_pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "strength_value",
    "therapeutic_class",
    "num_active_ingredients"
]

X_engineered = df[features_engineered].copy()
y_engineered = df["price_inr"].copy()

X_train_e, X_test_e, y_train_e, y_test_e = train_test_split(
    X_engineered,
    y_engineered,
    test_size=0.2,
    random_state=42
)

numeric_features_e = [
    "pack_size",
    "log_pack_size",
    "strength_value",
    "num_active_ingredients"
]

categorical_features_e = [
    "dosage_form",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "therapeutic_class"
]

preprocessor_e = ColumnTransformer([
    (
        "numeric",
        SimpleImputer(strategy="median"),
        numeric_features_e
    ),
    (
        "categorical",
        Pipeline([
            ("imputer", SimpleImputer(
                strategy="constant",
                fill_value="Unknown"
            )),
            ("encoder", OneHotEncoder(
                handle_unknown="ignore"
            ))
        ]),
        categorical_features_e
    )
])

rf_engineered = Pipeline([
    ("preprocessor", preprocessor_e),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])


# In[86]:


rf_engineered.fit(
    X_train_e,
    y_train_e
)

y_pred_e = rf_engineered.predict(X_test_e)


# In[87]:


mae_e = mean_absolute_error(
    y_test_e,
    y_pred_e
)

r2_e = r2_score(
    y_test_e,
    y_pred_e
)

print(f"MAE: ₹{mae_e:.2f}")
print(f"R²: {r2_e:.4f}")


# In[88]:


evaluation_e = pd.DataFrame({
    "actual": y_test_e.values,
    "predicted": y_pred_e
})

evaluation_e["absolute_error"] = (
    evaluation_e["actual"] - evaluation_e["predicted"]
).abs()

evaluation_e["price_range"] = pd.cut(
    evaluation_e["actual"],
    bins=[0, 100, 500, 2000, 10000, float("inf")],
    labels=[
        "₹0-100",
        "₹100-500",
        "₹500-2,000",
        "₹2,000-10,000",
        "₹10,000+"
    ]
)

range_performance_e = (
    evaluation_e
    .groupby("price_range", observed=True)
    .agg(
        medicine_count=("actual", "count"),
        mae=("absolute_error", "mean")
    )
)

range_performance_e


# In[89]:


percentage_errors_e = (
    np.abs(y_test_e.values - y_pred_e)
    / y_test_e.values
) * 100

mdape_e = np.median(percentage_errors_e)

print(f"MdAPE: {mdape_e:.2f}%")


# In[90]:


final_features = [
    "dosage_form",
    "pack_size",
    "log_pack_size",
    "pack_unit",
    "primary_ingredient",
    "primary_strength",
    "strength_value",
    "therapeutic_class",
    "num_active_ingredients"
]

X_final = df[final_features].copy()
y_final = df["price_inr"].copy()

final_model = Pipeline([
    (
        "preprocessor",
        preprocessor_e
    ),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
    )
])

final_model.fit(
    X_final,
    y_final
)

import joblib

from pathlib import Path

Path("../models").mkdir(exist_ok=True)

joblib.dump(
    final_model,
    "../models/medicine_price_model.joblib"
)


# In[91]:


from pathlib import Path

print(Path.cwd())

