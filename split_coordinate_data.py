import pandas as pd

# 엑셀 파일 경로
file_path = "/Users/yeonsu/Downloads/dongjak_db_y_x.xlsx"

# 각 시트 데이터 불러오기
acc_data = pd.read_excel(file_path, sheet_name="acc", header=0, usecols=["grsXCrd", "grsYCrd"])
cross_data = pd.read_excel(file_path, sheet_name="cross", header=0)

# 컬럼 이름 변경 (다루기 편하게)
acc_data.columns = ["acc_x", "acc_y"]

# acc_x가 먼저 오도록 순서 변경
acc_data = acc_data[["acc_x", "acc_y"]]  # acc_x가 첫 번째, acc_y가 두 번째로 설정

# 결과를 저장할 리스트
filtered_rows = []
non_filtered_rows = []

# 필터링: acc의 각 좌표와 cross의 좌표 비교
for _, acc_row in acc_data.iterrows():
    print(f"비교 중: acc 좌표 {acc_row['acc_x']}, {acc_row['acc_y']}")  # acc 데이터가 무엇인지 확인
    matched = False  # 일치하는 데이터가 있는지 추적
    for _, cross_row in cross_data.iterrows():
        # 두 좌표 간의 차이를 계산
        x_diff = abs(acc_row["acc_x"] - cross_row["grsXCrd"])
        y_diff = abs(acc_row["acc_y"] - cross_row["grsYCrd"])

        # 오차 범위 내인지 확인
        if x_diff <= 0.0009 and y_diff <= 0.0009:
            # 일치하는 cross 시트의 모든 데이터 추가
            filtered_rows.append({
                **acc_row.to_dict(),  # acc 시트의 데이터
                **cross_row.to_dict(),  # cross 시트의 모든 데이터
            })
            print(f"일치하는 cross 좌표: {cross_row['grsXCrd']}, {cross_row['grsYCrd']}")  # 일치하는 cross 좌표 출력
            matched = True  # 일치하는 데이터가 있으면 matched True로 설정

    # 일치하지 않으면 non_filtered_rows에 추가
    if not matched:
        # non_filtered_rows.append({**acc_row.to_dict(), **cross_row.to_dict()})
        non_filtered_rows.append(acc_row.to_dict())

# 필터링 결과를 DataFrame으로 변환
filtered_data = pd.DataFrame(filtered_rows)
non_filtered_data = pd.DataFrame(non_filtered_rows)

# 결과 저장
filtered_data.to_excel("filtered_split_coordinates.xlsx", index=False)
non_filtered_data.to_excel("nonmatched_split_coordinates.xlsx", index=False)

print(f"비교가 완료되었습니다. {len(filtered_rows)}개의 데이터가 필터링되었습니다.")
print(f"{len(non_filtered_rows)}개의 데이터는 조건에 맞지 않아서 따로 저장되었습니다.")
print("필터링 완료! 저장되었습니다.")
