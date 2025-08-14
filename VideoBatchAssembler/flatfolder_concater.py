import subprocess
from pathlib import Path

# ===== SETTINGS =====
sequence_dir = Path("./sequences")     # folder with .txt concat lists
output_video_dir = Path("./outputs")   # save final merged videos
output_video_dir.mkdir(exist_ok=True)

# ===== MAIN =====
txt_files = sorted(sequence_dir.glob("*.txt"))

if not txt_files:
    print(f"No .txt concat files found in {sequence_dir}")
    exit()

for txt_file in txt_files:
    # Detect extension from first listed clip
    with open(txt_file, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
    if not first_line.startswith("file "):
        print(f"⚠️ Skipping {txt_file.name} — invalid format")
        continue

    first_clip_name = first_line.replace("file '", "").rstrip("'")
    first_clip_path = Path(first_clip_name)

    if not first_clip_path.exists():
        print(f"⚠️ Skipping {txt_file.name} — {first_clip_name} not found in script folder")
        continue

    ext = first_clip_path.suffix or ".mp4"
    output_path = output_video_dir / f"{txt_file.stem}{ext}"

    print(f"Concatenating: {txt_file.name} -> {output_path.name}")

    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(txt_file),
        "-c", "copy",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)

print(f"\n✅ All sequences concatenated into: {output_video_dir}")

