import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_time.xlsx"

# 각 시트 데이터 불러오기
dongjak_data = pd.read_excel(file_path, sheet_name="dongjak", header=0, usecols=None)  # 모든 컬럼 불러오기
time_data = pd.read_excel(file_path, sheet_name="time", header=0, usecols=["accYmd", "accTime", "grsXCrd", "grsYCrd"])

if time_data["accYmd"].dtype != 'datetime64[ns]':
    time_data['accYmd'] = pd.to_datetime(time_data['accYmd'], origin='1899-12-30', unit='D')


# 컬럼 이름 변경 (다루기 편하게)
dongjak_data.columns = ["dongjak_" + col for col in dongjak_data.columns]  # dongjak 시트의 모든 컬럼 앞에 "dongjak_" 추가
time_data.columns = ["accYmd", "accTime", "time_x", "time_y"]

# 좌표가 일치하는 데이터를 필터링하여 time 시트에 추가하기
filtered_rows = []

for _, time_row in time_data.iterrows():
    print(f"비교 중: time 좌표 {time_row['time_x']}, {time_row['time_y']}")  # time 데이터 확인
    for _, dongjak_row in dongjak_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(time_row["time_x"] - dongjak_row["dongjak_grsXCrd"])
        y_diff = abs(time_row["time_y"] - dongjak_row["dongjak_grsYCrd"])

        print(f"  비교 중: dongjak 좌표 {dongjak_row['dongjak_grsXCrd']}, {dongjak_row['dongjak_grsYCrd']}")
        print(f"    x 차이: {x_diff}, y 차이: {y_diff}")

        # 오차 범위 내인지 확인
        if x_diff <= 0.0005 and y_diff <= 0.0005:
            # 일치하는 dongjak 시트의 모든 데이터를 time 시트에 추가
            combined_row = {**time_row.to_dict(), **dongjak_row.to_dict()}  # time 데이터와 dongjak 데이터 합치기
            filtered_rows.append(combined_row)
            print(f"    일치하는 데이터 발견!")
            print(f"    일치하는 dongjak 좌표: {dongjak_row['dongjak_grsXCrd']}, {dongjak_row['dongjak_grsYCrd']}")
            print(f"    추가된 데이터: {combined_row}")
        else:
            print(f"    오차 범위 밖: {x_diff}, {y_diff}")

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)

# 결과 저장
filtered_data.to_excel("a.xlsx", index=False)

print(f"비교가 완료되었습니다. {len(filtered_rows)}개의 데이터가 필터링되었습니다.")
print("필터링 완료! 결과가 'a.xlsx' 파일에 저장되었습니다.")
