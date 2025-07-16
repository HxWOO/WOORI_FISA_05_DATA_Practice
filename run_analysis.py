import pandas as pd
import os

# 데이터 디렉토리와 결과 디렉토리 경로 설정
data_dir = 'data'
results_dir = 'results'

# 결과 디렉토리가 없으면 생성
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# 데이터 디렉토리 내의 disable*.xlsx 파일 목록 가져오기
files_to_process = [f for f in os.listdir(data_dir) if f.startswith('disable') and f.endswith('.xlsx')]

# 각 파일 처리
for file_name in files_to_process:
    try:
        file_path = os.path.join(data_dir, file_name)
        
        # 엑셀 파일을 헤더 없이 읽기
        df = pd.read_excel(file_path, header=None)
        
        # 첫 두 행을 헤더로 사용
        header_row1 = df.iloc[0]
        header_row2 = df.iloc[1]
        
        new_columns = []
        current_year_period = ""
        for i, col_name_row2 in enumerate(header_row2):
            col_name_row1 = header_row1.iloc[i]
            
            # 첫 번째 컬럼 (구분별) 처리
            if i == 0:
                new_columns.append(str(col_name_row2).strip())
                continue

            # 첫 번째 행에 값이 있으면 새로운 연도/기간 시작
            if pd.notna(col_name_row1):
                current_year_period = str(col_name_row1).strip()

            # 컬럼 이름 조합
            if pd.notna(col_name_row2):
                combined_name = f"{current_year_period}_{str(col_name_row2).strip()}"
            else:
                combined_name = f"{current_year_period}_Unknown"
            
            new_columns.append(combined_name)

        # 새로운 컬럼 이름 설정 및 실제 데이터만 남기기
        df.columns = new_columns
        df = df.iloc[2:].copy() # 실제 데이터는 3번째 행부터 시작
        
        # 컬럼 이름에서 불필요한 공백이나 줄바꿈 문자 제거 (이미 strip 했지만 혹시 모를 경우)
        df.columns = df.columns.str.strip()
        
        # 결과 파일 경로 설정
        result_file_path = os.path.join(results_dir, f"processed_{file_name}")
        
        # 처리된 데이터프레임을 새로운 엑셀 파일로 저장 (인덱스 제외)
        df.to_excel(result_file_path, index=False)
        
        print(f"'{file_name}' 처리 완료 -> '{result_file_path}' 저장")

    except Exception as e:
        print(f"'{file_name}' 처리 중 오류 발생: {e}")

print("\n모든 파일 처리가 완료되었습니다.")