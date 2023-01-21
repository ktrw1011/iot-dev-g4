import json
from datetime import datetime
from argparse import ArgumentParser

from websocket import create_connection
import serial

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--serial", help="arduinoのシリアル通信しているポート名", required=True)
    parser.add_argument("-b", "--baudrate", help="arduinoで指定しているシリアル通信のボーレート", required=True)
    parser.add_argument("-u", "--utl", help="情報を送るURL", default="ws://localhost:8000/ws")

    args = parser.parse_args()
    
    # webサーバー側のwebソケットに接続
    # httpsサーバの場合はwssをに返る (例："wss://e15d-114-186-59-232.jp.ngrok.io/ws")
    ws = create_connection("ws://localhost:8000/ws")

    try:
        while True:
            # arduinoのメッセージを読み取る
            with serial.Serial(args.serial, args.baudrate, timeout=3) as ser:
                # arduinoからのメッセージはbyte型なのでデコードして改行を削除
                message: str = ser.readline().decode('utf-8').strip()
                # メッセージを表示
                print(f"Read message from arduino: {message}")

                if message != "":
                    # メッセージが空ではない場合はサーバーにメッセージを送る
                    json_data = json.dumps(
                        {
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "value": message,
                        }
                    )
                    # json文字列としてサーバーにデータを送る
                    ws.send(json_data)
                    # サーバーからの返信を受信
                    result =  ws.recv()
                    print(result)
            
    except KeyboardInterrupt:
        print("\nConnection closed")
        ws.close()

