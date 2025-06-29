import os
import subprocess

def convert_m4a_to_mp3(input_dir="inputs"):
    """
    指定されたディレクトリ内のm4aファイルをmp3に変換し、元のm4aファイルを削除します。
    """
    if not os.path.exists(input_dir):
        print(f"エラー: ディレクトリ '{input_dir}' が見つかりません。")
        return

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".m4a"):
            input_filepath = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".mp3"
            output_filepath = os.path.join(input_dir, output_filename)

            print(f"'{input_filepath}' を '{output_filepath}' に変換中...")

            try:
                # ffmpegコマンドを実行
                # -i: 入力ファイル
                # -vn: ビデオトラックを無効にする（オーディオのみを処理）
                # -acodec libmp3lame: MP3エンコーダとしてlibmp3lameを使用
                # -q:a 2: 可変ビットレート（VBR）品質設定。2は高品質（0が最高、9が最低）
                subprocess.run(
                    ["ffmpeg", "-i", input_filepath, "-vn", "-acodec", "libmp3lame", "-q:a", "2", output_filepath],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"'{input_filepath}' の変換が成功しました。")

                # 元のm4aファイルを削除
                os.remove(input_filepath)
                print(f"元のファイル '{input_filepath}' を削除しました。")

            except subprocess.CalledProcessError as e:
                print(f"エラー: '{input_filepath}' の変換に失敗しました。")
                print(f"FFmpegエラー出力:\n{e.stderr}")
            except FileNotFoundError:
                print("エラー: 'ffmpeg' コマンドが見つかりません。ffmpegがインストールされ、PATHが設定されていることを確認してください。")
                break
            except Exception as e:
                print(f"予期せぬエラーが発生しました: {e}")

if __name__ == "__main__":
    convert_m4a_to_mp3()

