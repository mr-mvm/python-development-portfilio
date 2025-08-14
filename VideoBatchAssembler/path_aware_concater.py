import subprocess
from pathlib import Path
import tempfile

# ===== SETTINGS =====
clips_dir = Path("./clips")            # base directory for video files
sequence_dir = Path("./sequences")     # .txt concat files with relative paths
output_video_dir = Path("./outputs")   # save final videos here
output_video_dir.mkdir(exist_ok=True)

# ===== MAIN =====
txt_files = sorted(sequence_dir.glob("*.txt"))

if not txt_files:
    print(f"No .txt concat files found in {sequence_dir}")
    exit()

for txt_file in txt_files:
    temp_txt = Path(tempfile.mktemp(suffix=".txt"))

    first_clip_path = None
    with open(txt_file, "r", encoding="utf-8") as f_in, open(temp_txt, "w", encoding="utf-8") as f_out:
        for line in f_in:
            if line.startswith("file "):
                clip_rel = line.strip().replace("file '", "").rstrip("'").replace("\\", "/")
                full_path = clips_dir / clip_rel
                if first_clip_path is None:
                    first_clip_path = full_path
                f_out.write(f"file '{full_path}'\n")

    if not first_clip_path or not first_clip_path.exists():
        print(f"⚠️ Skipping {txt_file.name} — first clip not found")
        continue

    ext = first_clip_path.suffix or ".mp4"
    output_path = output_video_dir / f"{txt_file.stem}{ext}

    print(f"Concatenating: {txt_file.name} -> {output_path.name}")

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(temp_txt),
        "-c", "copy",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)

print(f"\n✅ All sequences concatenated into: {output_video_dir}")

