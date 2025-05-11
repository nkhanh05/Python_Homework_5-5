import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import re

# Đọc dữ liệu
df = pd.read_csv('new_stat_table.csv',na_values=0)

features = df.columns[5:-1]

# Xử lý Price

df['Price'] = (
    df['Price'].astype(str)
    .str.replace('€', '', regex=False)
    .str.replace('M', '', regex=False)
    .str.replace('Free', '0', regex=False)
)

df['Price'] = pd.to_numeric(df['Price'], errors='coerce')


# Tạo X và y
X = df[features].fillna(0)
y = df['Price']

# Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Huấn luyện mô hình
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Dự đoán
y_pred = model.predict(X_test)

# Đánh giá
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:,.0f} €")
print(f"R² Score: {r2:.2f}")

# Hiển thị độ quan trọng của các đặc trưng
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop đặc trưng ảnh hưởng đến giá trị cầu thủ:")
with open("Anh_huong_cua_thong_so_toi_gia_chuyen_nhuong.txt",'w',encoding="utf-8") as last_file:
    print(f'{importance_df.to_string(index=False)}\n',file = last_file)
