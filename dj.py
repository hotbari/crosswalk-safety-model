import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_db_x_y.xlsx"

# 각 시트 데이터 불러오기
acc_data = pd.read_excel(file_path, sheet_name="acc", header=0, usecols=["grsXCrd", "grsYCrd"])
cross_data = pd.read_excel(file_path, sheet_name="cross", header=0)

# 컬럼 이름 변경 (다루기 편하게)
acc_data.columns = ["acc_y", "acc_x"]

# 결과를 저장할 리스트
filtered_rows = []

# 필터링: acc의 각 좌표와 cross의 좌표 비교
for _, acc_row in acc_data.iterrows():
    print(f"비교 중: acc 좌표 {acc_row['acc_x']}, {acc_row['acc_y']}")  # acc 데이터가 무엇인지 확인
    for _, cross_row in cross_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(acc_row["acc_x"] - cross_row["grsXCrd"])
        y_diff = abs(acc_row["acc_y"] - cross_row["grsYCrd"])

        # 오차 범위 내인지 확인
        if x_diff <= 0.0014 and y_diff <= 0.0014:
            # 일치하는 cross 시트의 모든 데이터 추가
            filtered_rows.append({
                **acc_row.to_dict(),  # acc 시트의 데이터
                **cross_row.to_dict(),  # cross 시트의 모든 데이터
            })
            print(f"일치하는 cross 좌표: {cross_row['grsXCrd']}, {cross_row['grsYCrd']}")  # 일치하는 cross 좌표 출력

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)

# 결과 저장
filtered_data.to_excel("dj_xy.xlsx", index=False)

print(f"비교가 완료되었습니다. {len(filtered_rows)}개의 데이터가 필터링되었습니다.")
print("필터링 완료! 저장도 완료!")
