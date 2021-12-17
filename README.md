# LSTM-based-Prediction-of-Bitcoin-Price-Fluctuation-using-Sentiment-Analysis

KICS2020.Fall에 게재된 'LSTM 기반 감성분석을 이용한 비트코인 가격 등락 예측'의 상세 파일들입니다.

# 개요

![image](https://user-images.githubusercontent.com/86222639/146499006-60464242-c2e6-4d2a-8101-c6e65fbc6934.png)

본 파일들은 
데이터 수집 - 데이터 클렌징 - 머신러닝 실험 순서에 따라

crawling - sentiment_analaysis - lstm 실험 으로 구성되어 있습니다.


#  데이터 수집

crawling 폴더의 serch.py를 이용해 2013.01.01 ~2020.07.30 사이의 키워드 '비트코인'에 대해 언급한 언론사를 count하여 비트코인 관련 영향력 있는 언론사 4개 선정

![image](https://user-images.githubusercontent.com/86222639/146498522-b3e0ff28-63bd-435a-b4e3-53310cb269cf.png)

해당 표를 바탕으로 coindesk, bitcoin News, coinTelegraph, Forbes 4개의 언론사에서 bitcoin에 대한 뉴스 
크롤링
(crawling 폴더의 DB_Forbes.py, DB_coindesk.py, DB_cointelegraph.py, bitcoin_com.py을 이용해 크롤링) 

# 데이터 클렌징

뉴스 기사의 감성분석 수치에 따라 비트코인의 가격이 변하는 것을 확인하기 위해 텍스트로 된 뉴스기사들을 감성수치 값으로 변환하는 과정입니다.

python 라이브러리 TextBlob을 이용해 전체 뉴스기사의 감성수치가 음수이면 부정적인 기사, 0이면 중립, 양수이면 긍정적인 기사로 count했습니다.

sentiment_analaysis 폴더의 to_excel.py를 이용해 긍정/부정적 기사 수 count, 평균값 도출

# 머신러닝 실험

LSTM모델을 통해 모델의 성능을 측정하고 그래프로 저장하는 부분입니다.

# 결과

![image](https://user-images.githubusercontent.com/86222639/146499890-72efbec0-8dfc-4c72-8ad9-af2ea18ec061.png)

훈련 셋 :1208, 테스트 셋:100개
hidden layer:2   hidden unit:4 일떄  58.75%의 정확도를 보여줌





