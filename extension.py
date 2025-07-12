import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# 1. 데이터 준비
file_path = "accYmdandtime.xlsx"

# 횡단보도와 사고 데이터 읽기
data = pd.read_excel(file_path, sheet_name="Sheet1", header=0, usecols=["accTime", "dongjak_횡단보도관리번호","dongjak_녹색신호시간","dongjak_적색신호시간"])

# 컬럼명 변경
data_renamed = data.rename(columns={
    "dongjak_횡단보도관리번호": "crosswalk_id",  # 횡단보도 관리번호
    "dongjak_녹색신호시간": "green_signal_time",  # 녹색 신호 시간
    "dongjak_적색신호시간": "red_signal_time",   # 적색 신호 시간
    "accTime": "accident_time"                  # 사고 발생 시간
})

print("=== 데이터 현황 ===")
print(data_renamed.head())
print(f"\n전체 데이터: {len(data_renamed)}행")
print(f"녹색신호시간 결측값: {data_renamed['green_signal_time'].isnull().sum()}개")
print(f"적색신호시간 결측값: {data_renamed['red_signal_time'].isnull().sum()}개")

# 사고 여부 컬럼 생성 (예시)
data_renamed['is_accident'] = (data_renamed['accident_time'] == 21).astype(int)

# 결측값 제거
data_renamed = data_renamed.dropna()

# 독립변수/종속변수 분리
X = data_renamed[["green_signal_time", "red_signal_time"]]
y = data_renamed["is_accident"]

print(f"\n=== 모델링 데이터 ===")
print(f"데이터 형태: X={X.shape}, y={y.shape}")
print(f"사고 발생률: {y.mean()*100:.2f}%")

# 3. 데이터셋 분리 (훈련 데이터와 테스트 데이터)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. 머신러닝 모델 훈련
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. 모델 평가
y_pred = model.predict(X_test)
print(f"\n=== 모델 성능 ===")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# 6. 녹색 신호 연장에 따른 사고율 분석
def predict_with_extension(extension):
    extended_data = X.copy()
    extended_data["green_signal_time"] += extension
    # 신호 비율 재계산
    extended_data["signal_ratio"] = extended_data["green_signal_time"] / (extended_data["green_signal_time"] + extended_data["red_signal_time"])
    # accident_time이 없으면 원본에서 복사
    if "accident_time" not in extended_data.columns:
        extended_data["accident_time"] = data_renamed["accident_time"].values
    # fit 시 사용한 feature 순서로 맞추기
    extended_data = extended_data[["green_signal_time", "red_signal_time", "accident_time", "signal_ratio"]]
    predictions = model.predict(extended_data)
    accident_rate = np.mean(predictions) * 100  # 사고 발생률(%)
    return accident_rate

# 기존 사고율
current_accident_rate = np.mean(y) * 100

print(f"\n=== 신호등 연장 효과 분석 ===")
print(f"현재 사고율: {current_accident_rate:.2f}%")

# 가장 위험한 횡단보도 찾기
dangerous_crosswalks = data_renamed[data_renamed['is_accident']==1].groupby('crosswalk_id').size().sort_values(ascending=False)
print(f"\n가장 위험한 횡단보도 (사고 발생 횟수):")
print(dangerous_crosswalks.head())
