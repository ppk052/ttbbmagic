LEFT_IRIS = [474, 475, 476, 477]  # 왼쪽 홍채를 구성하는 랜드마크 인덱스를 정의합니다.
RIGHT_IRIS = [469, 470, 471, 472]  # 오른쪽 홍채를 구성하는 랜드마크 인덱스를 정의합니다.
NOSE = [1, 2, 98, 327] #코&코주위 랜드마크

import asyncio
from server import WebSocketServer

async def main():
    server = WebSocketServer()  # 기본 호스트와 포트로 서버 생성
    await server.start()  # 서버 시작

if __name__ == "__main__":
    asyncio.run(main())




"""객체1
객체2
객체3
서버객체

서버객체.open
바로가기실행
서버객체.connencted=>boolean

객체1.open
객체2.open
객체3.open 선트래킹용



객체1.cor(RIGHT_IRIS)=>리턴값이 배열[0,0]
객체2.cor(RIGHT_IRIS)=>리턴값이 배열[0,0]
객체3.cor(~~)=>리턴값이 배열[0,0]

알고리즘~~~~~ 

알고리즘해야되는거
1. 디스플레이에 검정색출력할껀가
2. 디스플레이표시할 좌표

디스플레이좌표가 나왔어

서버객체.send(디스플레이좌표=>3차원배열)"""


