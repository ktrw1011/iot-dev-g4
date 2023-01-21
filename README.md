## インストール

```
pip install -r requirements.txt
```

## webサーバーの立ち上げ

デフォルトでローカルの8000番ポートで起動
```sh
uvicorn app:app
```

起動時の出力(URLにアクセスすれば画面が見れます)
```sh
INFO:     Started server process [38592]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## webサーバーにメッセージを送る例
webサーバーが起動している場合  
別のbashから以下のコマンドでメッセージを送れます  
グラフの値が変化することが分かります
```
python send_data_example.py
```

```python
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
```

