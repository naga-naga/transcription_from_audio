# transcription_from_audio
音声ファイルから文字起こしする

## 使い方
```
python transcribe.py <audio file>
```
とするとコンソールに出力．

```
python transcribe.py <audio file> [output]
```
とすると`output`に出力．

多分 wav ファイルしか文字起こしできない．

## 例
```
python transcribe.py hoge.wav
>>> hoge.wav の内容を文字に起こしてコンソールに出力
```

```
python transcribe.py hoge.wav output.txt
>>> hoge.wav の内容を文字に起こして output.txt に出力
```