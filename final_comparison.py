import pandas as pd
import numpy as np

def final_comparison(file1, file2):
    print(f"=== {file1} vs {file2} 최종 비교 ===\n")
    
    # 파일 읽기
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    print("1. 완전한 동등성 검사:")
    
    # 모든 컬럼에 대해 정확히 같은지 확인
    all_equal = True
    differences = []
    
    for col in df1.columns:
        if col in df2.columns:
            # NaN 값을 포함한 정확한 비교
            if not df1[col].equals(df2[col]):
                all_equal = False
                # 차이가 있는 행 수 계산
                diff_count = (~(df1[col] == df2[col]) | (df1[col].isna() != df2[col].isna())).sum()
                differences.append(f"   - {col}: {diff_count}개 행에서 차이")
    
    if all_equal:
        print("   ✓ 두 파일의 모든 데이터가 완전히 동일합니다.")
    else:
        print("   ✗ 두 파일에 차이가 있습니다:")
        for diff in differences:
            print(diff)
    print()
    
    print("2. 파일 메타데이터 비교:")
    print(f"   {file1}:")
    print(f"     - 행 수: {len(df1)}")
    print(f"     - 열 수: {len(df1.columns)}")
    print(f"     - 메모리 사용량: {df1.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print(f"   {file2}:")
    print(f"     - 행 수: {len(df2)}")
    print(f"     - 열 수: {len(df2.columns)}")
    print(f"     - 메모리 사용량: {df2.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print()
    
    print("3. 데이터 요약:")
    print("   두 파일 모두 동작구 횡단보도 데이터로 보이며:")
    print(f"   - 총 {len(df1)}개의 횡단보도 정보")
    print(f"   - {len(df1.columns)}개의 속성 정보")
    print(f"   - 좌표 범위: 위도 {df1['acc_x'].min():.6f}~{df1['acc_x'].max():.6f}, 경도 {df1['acc_y'].min():.6f}~{df1['acc_y'].max():.6f}")
    print()
    
    print("4. 결론:")
    if all_equal:
        print("   두 파일은 완전히 동일한 데이터를 포함하고 있습니다.")
        print("   파일명만 다르고 내용은 100% 일치합니다.")
    else:
        print("   두 파일에 차이가 있습니다.")
        print("   위의 차이점을 참고하시기 바랍니다.")

if __name__ == "__main__":
    final_comparison("dj_xy.xlsx", "dj_x_y.xlsx") 