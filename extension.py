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

# 결측값이 있는 행 제거
data_renamed = data_renamed.dropna()
print(f"결측값 제거 후 데이터: {len(data_renamed)}행")

# 사고 여부 판단 (더 현실적인 기준)
# 1. 시간대별 위험도 (야간 시간대가 더 위험)
# 2. 신호 시간 비율 (녹색/적색 신호 비율이 낮을수록 위험)
data_renamed['is_night'] = (data_renamed['accident_time'] >= 22) | (data_renamed['accident_time'] <= 6)
data_renamed['signal_ratio'] = data_renamed['green_signal_time'] / (data_renamed['green_signal_time'] + data_renamed['red_signal_time'])
data_renamed['is_accident'] = (
    (data_renamed['is_night'] & (data_renamed['signal_ratio'] < 0.3)) |  # 야간 + 짧은 녹색신호
    (data_renamed['accident_time'] == 21) |  # 21시 (피크 시간)
    (data_renamed['signal_ratio'] < 0.2)     # 매우 짧은 녹색신호
).astype(int)

# 2. 독립 변수(X)와 종속 변수(y) 분리
X = data_renamed[["green_signal_time", "red_signal_time", "accident_time", "signal_ratio"]]
y = data_renamed["is_accident"]

print(f"\n=== 모델링 데이터 ===")
print(f"데이터 형태: X={X.shape}, y={y.shape}")
print(f"사고 발생률: {y.mean()*100:.2f}%")
print(f"야간 사고 비율: {data_renamed[data_renamed['is_accident']==1]['is_night'].mean()*100:.2f}%")

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
    """
    녹색 신호를 연장했을 때 사고 여부 예측
    """
    extended_data = X.copy()
    extended_data["green_signal_time"] += extension
    # 신호 비율 재계산
    extended_data["signal_ratio"] = extended_data["green_signal_time"] / (extended_data["green_signal_time"] + extended_data["red_signal_time"])
    predictions = model.predict(extended_data)
    accident_rate = np.mean(predictions) * 100  # 사고 발생률(%)
    return accident_rate

# 기존 사고율
current_accident_rate = np.mean(y) * 100

print(f"\n=== 신호등 연장 효과 분석 ===")
print(f"현재 사고율: {current_accident_rate:.2f}%")

# 다양한 연장 시간에 대한 효과 분석
print(f"\n=== 다양한 연장 시간별 효과 ===")
for extension in [5, 10, 15, 20, 30]:
    rate = predict_with_extension(extension)
    reduction = current_accident_rate - rate
    print(f"연장 {extension:2d}초: 사고율 {rate:5.2f}% (감소 {reduction:5.2f}%)")

# 7. 추가 분석
print(f"\n=== 상세 분석 ===")
print("현재 신호 시간 통계:")
print(f"  녹색신호 평균: {data_renamed['green_signal_time'].mean():.1f}초")
print(f"  적색신호 평균: {data_renamed['red_signal_time'].mean():.1f}초")
print(f"  신호비율 평균: {data_renamed['signal_ratio'].mean():.3f}")

# 가장 위험한 횡단보도 찾기
dangerous_crosswalks = data_renamed[data_renamed['is_accident']==1].groupby('crosswalk_id').size().sort_values(ascending=False)
print(f"\n가장 위험한 횡단보도 (사고 발생 횟수):")
print(dangerous_crosswalks.head())
