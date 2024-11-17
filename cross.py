import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_db.xlsx"

# 각 시트 데이터 불러오기
acc_data = pd.read_excel(file_path, sheet_name="acc", header=0, usecols=["grsXCrd", "grsYCrd"])
cross_data = pd.read_excel(file_path, sheet_name="cross", header=0, usecols=["grsXCrd", "grsYCrd"])

# 컬럼 이름 변경 (다루기 편하게)
acc_data.columns = ["acc_x", "acc_y"]
cross_data.columns = ["cross_x", "cross_y"]

# 결과를 저장할 리스트
filtered_rows = []

# 필터링: acc의 각 좌표와 cross의 좌표 비교
print("필터링 시작...")

# 필터링: acc의 각 좌표와 cross의 좌표 비교
for acc_index, acc_row in acc_data.iterrows():
    for cross_index, cross_row in cross_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(acc_row["acc_x"] - cross_row["cross_x"])
        y_diff = abs(acc_row["acc_y"] - cross_row["cross_y"])

        # 디버깅: 현재 비교 중인 좌표와 차이값 출력
        print(f"비교: acc[{acc_index}]({acc_row['acc_x']}, {acc_row['acc_y']}) "
              f"<-> cross[{cross_index}]({cross_row['cross_x']}, {cross_row['cross_y']})")
        print(f"x_diff: {x_diff}, y_diff: {y_diff}")

        # 오차 범위 내인지 확인
        if x_diff <= 1 and y_diff <= 1:
            print(f"조건 만족: acc[{acc_index}] <-> cross[{cross_index}]")
            filtered_rows.append({
                "acc_x": acc_row["acc_x"],
                "acc_y": acc_row["acc_y"],
                "cross_x": cross_row["cross_x"],
                "cross_y": cross_row["cross_y"],
            })

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)

# 결과 데이터 확인
print(f"필터링된 데이터 개수: {len(filtered_rows)}")
if not filtered_rows:
    print("필터링된 데이터가 없습니다. 조건을 확인하세요.")
else:
    print("필터링된 데이터 샘플:")
    print(filtered_data.head())

# 결과 저장
filtered_data.to_excel("filtered_results.xlsx", index=False)

print("필터링 완료! 결과는 파일에 저장되었습니다.")
