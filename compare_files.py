import pandas as pd
import numpy as np

def compare_excel_files(file1, file2):
    print(f"=== {file1} vs {file2} 비교 분석 ===\n")
    
    # 파일 읽기
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    print(f"1. 기본 정보 비교:")
    print(f"   {file1}: {df1.shape[0]}행 x {df1.shape[1]}열")
    print(f"   {file2}: {df2.shape[0]}행 x {df2.shape[1]}열")
    print(f"   행 수 차이: {abs(df1.shape[0] - df2.shape[0])}")
    print(f"   열 수 차이: {abs(df1.shape[1] - df2.shape[1])}\n")
    
    print(f"2. 컬럼 비교:")
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    
    if cols1 == cols2:
        print("   ✓ 두 파일의 컬럼이 동일합니다.")
    else:
        print("   ✗ 두 파일의 컬럼이 다릅니다.")
        print(f"   {file1}에만 있는 컬럼: {cols1 - cols2}")
        print(f"   {file2}에만 있는 컬럼: {cols2 - cols1}")
    print()
    
    # 공통 컬럼이 있는 경우 데이터 비교
    common_cols = cols1.intersection(cols2)
    if common_cols:
        print(f"3. 데이터 비교 (공통 컬럼 {len(common_cols)}개):")
        
        # 각 컬럼별로 차이점 분석
        differences = []
        for col in common_cols:
            if df1[col].dtype != df2[col].dtype:
                differences.append(f"   - {col}: 데이터 타입이 다름 ({df1[col].dtype} vs {df2[col].dtype})")
            elif not df1[col].equals(df2[col]):
                # 값이 다른 행 수 계산
                diff_count = (df1[col] != df2[col]).sum()
                if diff_count > 0:
                    differences.append(f"   - {col}: {diff_count}개 행에서 값이 다름")
        
        if differences:
            print("   발견된 차이점:")
            for diff in differences:
                print(diff)
        else:
            print("   ✓ 두 파일의 데이터가 완전히 동일합니다.")
        print()
    
    # 좌표 데이터 특별 분석 (acc_x, acc_y, grsXCrd, grsYCrd)
    coord_cols = ['acc_x', 'acc_y', 'grsXCrd', 'grsYCrd']
    coord_cols_exist = [col for col in coord_cols if col in common_cols]
    
    if coord_cols_exist:
        print(f"4. 좌표 데이터 분석:")
        for col in coord_cols_exist:
            if col in df1.columns and col in df2.columns:
                # 좌표 값의 통계 정보
                print(f"   {col} 통계:")
                print(f"     {file1}: min={df1[col].min():.6f}, max={df1[col].max():.6f}, mean={df1[col].mean():.6f}")
                print(f"     {file2}: min={df2[col].min():.6f}, max={df2[col].max():.6f}, mean={df2[col].mean():.6f}")
                
                # 좌표 값이 다른 행 수
                diff_coords = (df1[col] != df2[col]).sum()
                print(f"     차이: {diff_coords}개 행")
                print()
    
    # 중복 데이터 분석
    print(f"5. 중복 데이터 분석:")
    print(f"   {file1} 중복 행: {df1.duplicated().sum()}개")
    print(f"   {file2} 중복 행: {df2.duplicated().sum()}개")
    print()
    
    # 결측값 분석
    print(f"6. 결측값 분석:")
    print(f"   {file1} 결측값:")
    for col in df1.columns:
        missing = df1[col].isnull().sum()
        if missing > 0:
            print(f"     {col}: {missing}개")
    
    print(f"   {file2} 결측값:")
    for col in df2.columns:
        missing = df2[col].isnull().sum()
        if missing > 0:
            print(f"     {col}: {missing}개")
    print()

if __name__ == "__main__":
    compare_excel_files("dj_xy.xlsx", "dj_x_y.xlsx") 