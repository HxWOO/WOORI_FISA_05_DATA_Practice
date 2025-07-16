import pandas as pd
import os

def load_processed_data():
    """
    'results' 디렉토리에서 처리된 엑셀 파일들을 읽어
    pandas DataFrame 딕셔너리로 반환합니다.
    
    Returns:
        dict: 파일 이름을 키로, DataFrame을 값으로 하는 딕셔너리.
              오류 발생 시 None을 반환합니다.
    """
    results_dir = 'results'
    dataframes = {}

    # results 디렉토리 존재 여부 확인
    if not os.path.exists(results_dir):
        print(f"오류: '{results_dir}' 디렉토리를 찾을 수 없습니다.")
        return None

    # 처리된 엑셀 파일 목록 가져오기
    files_to_load = [f for f in os.listdir(results_dir) if f.startswith('processed_') and f.endswith('.xlsx')]

    if not files_to_load:
        print(f"'{results_dir}' 디렉토리에서 처리된 파일을 찾을 수 없습니다.")
        return None

    print("처리된 엑셀 파일들을 DataFrame으로 불러옵니다...")
    
    # 각 파일을 DataFrame으로 읽어 딕셔너리에 저장
    for file_name in files_to_load:
        try:
            file_path = os.path.join(results_dir, file_name)
            # 'processed_' 접두사와 '.xlsx' 확장자를 제거하여 딕셔너리 키 생성
            df_key = file_name.replace('processed_', '').replace('.xlsx', '')
            
            dataframes[df_key] = pd.read_excel(file_path)
            print(f"- '{file_name}' 로드 완료 -> key: '{df_key}'")

        except Exception as e:
            print(f"'{file_name}' 파일을 불러오는 중 오류 발생: {e}")
    
    print("\n모든 데이터를 성공적으로 불러왔습니다.")
    return dataframes

if __name__ == '__main__':
    # 함수를 실행하여 데이터프레임들을 불러옵니다.
    all_dataframes = load_processed_data()

    # 데이터가 성공적으로 로드되었는지 확인하고 정보 출력
    if all_dataframes:
        print("\n--- 각 DataFrame 정보 요약 ---")
        for name, df in all_dataframes.items():
            print(f"\nDataFrame '{name}':")
            print(f"  - 행: {df.shape[0]}, 열: {df.shape[1]}")
            print("  - 첫 5행 데이터:")
            print(df.head())
            
        # 예시: 'disable_age' 데이터프레임 접근 방법
        # if 'disable_age' in all_dataframes:
        #     print("\n--- 'disable_age' DataFrame 샘플 ---")
        #     print(all_dataframes['disable_age'].head())

