import time
import json
import random
from datetime import datetime
from argparse import ArgumentParser
from websocket import create_connection

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-u", "--utl", help="情報を送るURL", default="ws://localhost:8000/ws")
    
    args = parser.parse_args()
    
    # webサーバー側のwebソケットに接続
    # httpsサーバの場合はwssをに返る (例："wss://e15d-114-186-59-232.jp.ngrok.io/ws")
    ws = create_connection("ws://localhost:8000/ws")

    try:
        while True:
            time.sleep(1)
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "value": random.random() * 100,
                }
            )
            # json文字列を受け取る
            ws.send(json_data)
            # サーバーからの返信を受信
            result =  ws.recv()
            print(result)
            
    except KeyboardInterrupt:
        # コネクションを閉じる
        print("\nConnection closed")
        ws.close()