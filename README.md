# portable-faster-whisper
## 手順
### mp3変換
m4aファイルをmp3ファイルにする
```shell
task convert-audio
```

### 文字起こし
文字起こししたいファイルを指定して、main.pyを実行する
→output配下にテキストファイルが生成される
```shell
task bash
python main.py {ファイル名}.mp3
```
