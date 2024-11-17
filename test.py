import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_time.xlsx"

# 각 시트 데이터 불러오기
dongjak_data = pd.read_excel(file_path, sheet_name="dongjak", header=0, usecols=["grsXCrd", "grsYCrd"])
time_data = pd.read_excel(file_path, sheet_name="time", header=0, usecols=["accYmd", "accTime", "grsXCrd", "grsYCrd"])

# accYmd가 숫자형일 경우 변환 (엑셀 날짜 형식으로 저장된 경우 처리)
if time_data["accYmd"].dtype == 'float64':  # accYmd가 숫자형인 경우
    time_data['accYmd'] = pd.to_datetime(time_data['accYmd'], origin='1899-12-30', unit='D')

# 컬럼 이름 변경 (다루기 편하게)
dongjak_data.columns = ["dongjak_x", "dongjak_y"]
time_data.columns = ["accYmd", "accTime", "time_x", "time_y"]

# 결과를 저장할 리스트
filtered_rows = []

# 필터링: time의 각 좌표와 dongjak의 좌표 비교
for _, time_row in time_data.iterrows():
    print(f"비교 중: time 좌표 {time_row['time_x']}, {time_row['time_y']}")  # time 데이터 확인
    for _, dongjak_row in dongjak_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(time_row["time_x"] - dongjak_row["dongjak_x"])
        y_diff = abs(time_row["time_y"] - dongjak_row["dongjak_y"])

        # 오차 범위 내인지 확인
        if x_diff <= 0.0005 and y_diff <= 0.0005:
            filtered_rows.append({
                **time_row.to_dict(),  # time 시트의 데이터
                **dongjak_row.to_dict(),  # dongjak 시트의 데이터
            })
            print(f"일치하는 dongjak 좌표: {dongjak_row['dongjak_x']}, {dongjak_row['dongjak_y']}")  # 일치하는 dongjak 좌표 출력

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)

# 결과 저장
filtered_data.to_excel("filtered_result_with_dates.xlsx", index=False)

print(f"비교가 완료되었습니다. {len(filtered_rows)}개의 데이터가 필터링되었습니다.")
print("필터링 완료! 저장도 완료!")
