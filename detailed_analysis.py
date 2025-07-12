import pandas as pd
import numpy as np

def detailed_analysis(file1, file2):
    print(f"=== {file1} vs {file2} 상세 분석 ===\n")
    
    # 파일 읽기
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    print("1. 파일 해시값 비교 (파일이 완전히 동일한지 확인):")
    # 각 데이터프레임을 문자열로 변환하여 해시값 계산
    hash1 = hash(str(df1.values.tobytes()))
    hash2 = hash(str(df2.values.tobytes()))
    
    if hash1 == hash2:
        print("   ✓ 두 파일의 데이터가 완전히 동일합니다.")
    else:
        print("   ✗ 두 파일의 데이터가 다릅니다.")
    print()
    
    print("2. 각 컬럼별 데이터 타입 비교:")
    for col in df1.columns:
        dtype1 = df1[col].dtype
        dtype2 = df2[col].dtype
        if dtype1 != dtype2:
            print(f"   {col}: {dtype1} vs {dtype2}")
        else:
            print(f"   {col}: {dtype1} ✓")
    print()
    
    print("3. 좌표 데이터 상세 분석:")
    coord_cols = ['acc_x', 'acc_y', 'grsXCrd', 'grsYCrd']
    
    for col in coord_cols:
        if col in df1.columns:
            print(f"   {col}:")
            print(f"     {file1} - 최소값: {df1[col].min():.8f}, 최대값: {df1[col].max():.8f}")
            print(f"     {file2} - 최소값: {df2[col].min():.8f}, 최대값: {df2[col].max():.8f}")
            
            # 값이 다른 행 찾기
            diff_mask = df1[col] != df2[col]
            if diff_mask.any():
                diff_indices = diff_mask[diff_mask].index
                print(f"     차이: {len(diff_indices)}개 행")
                print(f"     차이가 있는 행 번호: {list(diff_indices[:5])}...")  # 처음 5개만 표시
            else:
                print(f"     ✓ 완전히 동일")
            print()
    
    print("4. 데이터 품질 분석:")
    
    # 고유값 개수 비교
    print("   고유값 개수 비교:")
    for col in df1.columns:
        unique1 = df1[col].nunique()
        unique2 = df2[col].nunique()
        if unique1 != unique2:
            print(f"     {col}: {unique1} vs {unique2}")
        else:
            print(f"     {col}: {unique1} ✓")
    print()
    
    # 결측값 상세 분석
    print("   결측값 상세 분석:")
    for col in df1.columns:
        missing1 = df1[col].isnull().sum()
        missing2 = df2[col].isnull().sum()
        if missing1 > 0 or missing2 > 0:
            print(f"     {col}: {missing1} vs {missing2} (총 {df1.shape[0]}행 중)")
    print()
    
    print("5. 데이터 분포 비교 (수치형 컬럼):")
    numeric_cols = df1.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        if col in df1.columns and col in df2.columns:
            print(f"   {col}:")
            print(f"     {file1} - 평균: {df1[col].mean():.6f}, 표준편차: {df1[col].std():.6f}")
            print(f"     {file2} - 평균: {df2[col].mean():.6f}, 표준편차: {df2[col].std():.6f}")
            
            # 분포가 다른지 확인
            if abs(df1[col].mean() - df2[col].mean()) > 1e-10:
                print(f"     ✗ 평균값이 다름")
            else:
                print(f"     ✓ 평균값 동일")
            print()
    
    print("6. 파일 크기 및 메모리 사용량:")
    print(f"   {file1} 메모리 사용량: {df1.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print(f"   {file2} 메모리 사용량: {df2.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print()

if __name__ == "__main__":
    detailed_analysis("dj_xy.xlsx", "dj_x_y.xlsx") 