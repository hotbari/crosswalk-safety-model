import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_db_x_y.xlsx"

# 각 시트 데이터 불러오기
acc_data = pd.read_excel(file_path, sheet_name="acc", header=0, usecols=["L", "M"])  # acc 시트의 L, M 열
cross_data = pd.read_excel(file_path, sheet_name="cross", header=0, usecols=["I", "J"])  # cross 시트의 I, J 열

# 컬럼 이름 변경 (다루기 편하게)
acc_data.columns = ["acc_x", "acc_y"]  # acc 시트의 좌표 컬럼 이름 변경
cross_data.columns = ["cross_x", "cross_y"]  # cross 시트의 좌표 컬럼 이름 변경

# 결과를 저장할 리스트
filtered_rows = []

# 필터링: acc의 각 좌표와 cross의 좌표 비교
for _, acc_row in acc_data.iterrows():
    for _, cross_row in cross_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(acc_row["acc_x"] - cross_row["cross_x"])
        y_diff = abs(acc_row["acc_y"] - cross_row["cross_y"])

        # 오차 범위 내인지 확인
        if x_diff <= 0.0014 and y_diff <= 0.0014:
            # acc 데이터와 cross 데이터 모두 추가
            filtered_rows.append({
                **acc_row.to_dict(),  # acc 시트의 좌표 데이터
                **cross_row.to_dict(),  # cross 시트의 좌표 데이터
            })

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)

# 결과 저장
filtered_data.to_excel("x_y_fixx.xlsx", index=False)

print("필터링 완료! 결과는 'filtered_results.xlsx' 파일에 저장되었습니다.")
