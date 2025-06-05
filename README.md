# invest 확인 프로그램
2. **분석 결과** - 입력값을 토대로 요약과 간단한 피드백과 간단한 리스크 지표를 보여줍니다.
이 버전에서는 Python으로 작성된 작은 백엔드(`server.py`)를 제공하여
입력된 거래 내역을 `history.json` 파일에 저장하고, 누적 데이터로부터
매우 단순한 Value at Risk(VaR) 지표를 계산합니다.

서버 실행 방법:

```bash
python3 server.py
```

브라우저에서 `http://localhost:8000`으로 접속하면 웹 앱을 이용할 수 있습니다.
