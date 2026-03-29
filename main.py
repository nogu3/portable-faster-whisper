import argparse
import os
from faster_whisper import WhisperModel

def parse_args():
    parser = argparse.ArgumentParser(description='Transcribe audio file using Faster Whisper')
    parser.add_argument('input_file', nargs='+', help='Input audio filenames (e.g., audio1.mp3 audio2.mp3). Assumed to be in the "inputs" directory.')
    return parser.parse_args()

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(
    model_size,
    device="cuda",
    compute_type="float16",
    # compute_type="float32",
    device_index=0,  # 明示的にGPU 0を指定
    num_workers=2,    # 並列処理を有効化
    download_root="/workspace/.cache/models"
)

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")

# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

default_parameters = {
    "beam_size": 5,
}

fast_parameters = {
    "beam_size": 1,                    # 最速
    "best_of": 1,                      # 最速
    "temperature": 0.0,                # 決定的
    "vad_filter": True,                # 無音スキップ
    "without_timestamps": True,        # タイムスタンプ無し
    "condition_on_previous_text": False, # 前文脈無視
    "compression_ratio_threshold": 3.0,  # 緩いフィルタ
    "log_prob_threshold": -0.5,        # 緩いフィルタ
    "suppress_blank": True,            # 空白抑制
    "max_new_tokens": 224              # トークン制限
}

japanese_parameters = {
    "language": "ja",                  # 言語を明示指定（自動検出をやめる）
    "beam_size": 10,                   # 候補を多く探索（精度重視）
    "best_of": 1,
    "temperature": 0.0,
    "vad_filter": True,                # 無音スキップ（ハルシネーション防止のため有効化）
    "vad_parameters": {
        "threshold": 0.1,              # 音声検出の閾値を大幅に下げる
        "min_speech_duration_ms": 50,
        "min_silence_duration_ms": 2000,
    },
    "without_timestamps": False,       # タイムスタンプ有効化
    "condition_on_previous_text": False, # Trueにすると同一フレーズが連鎖するリスクがある
    "suppress_blank": True,            # 空白抑制
    "initial_prompt": "以下は日本語の住宅に関する打ち合わせや説明の音声です。正確に文字起こししてください。句読点（、。）を適切に使用してください。",
}

parameters = japanese_parameters

args = parse_args()

# Construct the full path to the input file in the 'inputs' directory
input_dir = "inputs"

output_dir = "outputs"

for input_file in args.input_file:
    full_input_file_path = os.path.join(input_dir, input_file)

    segments, info = model.transcribe(
        full_input_file_path, 
        **parameters,
    )

    print(f"Detected language '{info.language}' with probability {info.language_probability}")

    # 入力ファイル名から出力ファイル名を生成
    input_filename = input_file
    output_filename = os.path.join(output_dir, f"{input_filename.rsplit('.', 1)[0]}_transcript.txt")

    # 全セグメントのテキストを準備
    output_text = [f"Detected language: {info.language} (probability: {info.language_probability:.2f})\n\n"]

    for segment in segments:
        start_time = f"{int(segment.start // 60):02d}:{int(segment.start % 60):02d}"
        end_time = f"{int(segment.end // 60):02d}:{int(segment.end % 60):02d}"
        line = f"[{start_time} -> {end_time}] {segment.text}"
        
        # コンソールに出力
        print(line)
        
        # 出力テキストに追加
        output_text.append(line)

    # 全てのテキストを一度にファイルに書き込み
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(output_text))
