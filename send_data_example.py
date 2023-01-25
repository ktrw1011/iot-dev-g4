import time
import json
import random
from datetime import datetime
from argparse import ArgumentParser
from websocket import create_connection

def gen_sample_data():
    res = []
    for _ in range(10):
        time.sleep(0.5)
        res.append(
            {
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "uid": "1453317129",
                "menu": "rice",
                "bite_power": random.random() * 100,
                "bite_count": random.random() * 100,
                "bite_p_th": random.random() * 100,
                "bite_c_th": random.random() * 100,
        })
    return res

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
            json_data = json.dumps(gen_sample_data())
            # json文字列を受け取る
            ws.send(json_data)
            # サーバーからの返信を受信
            result =  ws.recv()
            print(result)
            
    except KeyboardInterrupt:
        # コネクションを閉じる
        print("\nConnection closed")
        ws.close()