import pandas as pd
import os
import requests
import json

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

def load_disabled_population_data():
    """
    'korean_disabled_population_statistics.csv' 파일을 읽어 전처리 후 DataFrame으로 반환합니다.
    
    Returns:
        pd.DataFrame: 전처리된 장애인구 통계 데이터.
                      오류 발생 시 None을 반환합니다.
    """
    file_path = os.path.join('data', 'korean_disabled_population_statistics.csv')
    
    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None
        
    try:
        df = pd.read_csv(file_path)
        
        # 전처리: '-' 값을 0으로 채우고, 연도 컬럼을 정수형으로 변환
        df.replace('-', 0, inplace=True)
        for col in df.columns[3:]:
            df[col] = df[col].astype(int)
            
        print(f"'{file_path}' 로드 및 전처리 완료.")
        return df
        
    except Exception as e:
        print(f"'{file_path}' 파일을 불러오거나 전처리하는 중 오류 발생: {e}")
        return None

def load_korea_geojson(file_name="skorea_provinces_geo.json"):
    """
    한국 시도별 GeoJSON 파일을 로드합니다. 파일이 없으면 다운로드합니다.
    """
    geojson_path = os.path.join('data', file_name)
    
    if not os.path.exists(geojson_path):
        # st.info(f"{file_name} 파일을 다운로드합니다...") # Removed streamlit dependency
        print(f"Downloading {file_name}...")
        url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/korea_administrative_boundaries/2018/geojson/skorea_provinces_geo.json"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
            with open(geojson_path, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            # st.success(f"{file_name} 다운로드 완료.") # Removed streamlit dependency
            print(f"Successfully downloaded {file_name}.")
        except requests.exceptions.RequestException as e:
            # st.error(f"GeoJSON 파일 다운로드 중 오류 발생: {e}") # Removed streamlit dependency
            print(f"Error downloading GeoJSON file: {e}")
            return None

    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    return geojson_data

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
            
    # 장애인구 통계 데이터 로드 및 정보 출력
    disabled_df = load_disabled_population_data()
    if disabled_df is not None:
        print("\n--- 장애인구 통계 DataFrame 정보 요약 ---")
        print(f"  - 행: {disabled_df.shape[0]}, 열: {disabled_df.shape[1]}")
        print("  - 첫 5행 데이터:")
        print(disabled_df.head())
        print("  - 컬럼별 데이터 타입:")
        print(disabled_df.info())

    # GeoJSON 데이터 로드 및 정보 출력
    geojson_data = load_korea_geojson()
    if geojson_data:
        print("\n--- GeoJSON 데이터 로드 완료 ---")
        print(f"GeoJSON features: {len(geojson_data['features'])}")

