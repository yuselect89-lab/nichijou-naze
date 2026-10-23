#!/usr/bin/env python3
"""日常のなぜ？: video technical PDCA gate.
Needs Python stdlib + ffmpeg/ffprobe. This is NOT a visual-quality/G3 verdict.
Usage: python3 tools/visual_pdca_qc.py --config episodes/EPxxx/visual_pdca_case.json --out episodes/EPxxx/visual_pdca_report.json
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def cmd(arguments):
    completed = subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if completed.returncode:
        raise RuntimeError(" ".join(str(a) for a in arguments) + "\n" + completed.stderr.decode("utf-8", "replace")[-900:])
    return completed.stdout


def motion_diff(video, a, b, roi):
    x, y, w, h = roi
    vf = f"crop={w}:{h}:{x}:{y},scale=160:180,format=gray"

    def get_frame(t):
        return cmd(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-vf", vf,
                    "-frames:v", "1", "-f", "rawvideo", "pipe:1"])

    first, second = get_frame(a), get_frame(b)
    if not first or len(first) != len(second):
        raise ValueError("Could not read comparable frames")
    return round(sum(abs(p - q) for p, q in zip(first, second)) / len(first), 4)


def srt_text(path):
    cues = []
    for block in re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) >= 3:
            cues.append("\n".join(lines[2:]))
    return cues


def normalize(s):
    return re.sub(r"[\s、。？！?!「」『』：:・,．.]", "", s)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", required=True)
    opts = parser.parse_args()

    config_path = Path(opts.config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    base = config_path.parent

    def locate(p):
        file = Path(p)
        return file if file.is_absolute() else (base / file).resolve()

    candidate = locate(config["candidate"])
    checks = {}
    observations = {}

    def check(key, passed, detail):
        checks[key] = {"status": "PASS" if passed else "FAIL", "detail": detail}

    try:
        info = json.loads(cmd(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(candidate)]))
        video = [s for s in info["streams"] if s["codec_type"] == "video"]
        audio = [s for s in info["streams"] if s["codec_type"] == "audio"]
        v = video[0] if video else {}
        duration = float(info["format"].get("duration", 0))
        frames = int(v.get("nb_frames", 0))
        expected_fps = config.get("fps", "30/1")
        valid_format = (len(video) == 1 and len(audio) == 1
                        and v.get("width") == config["width"] and v.get("height") == config["height"]
                        and frames == config["frames"] and v.get("r_frame_rate") == expected_fps
                        and abs(duration - config["duration"]) < 0.05)
        check("format", valid_format, {"duration": duration, "frames": frames, "fps": v.get("r_frame_rate"),
                                      "video_codec": v.get("codec_name"), "audio_codec": audio[0].get("codec_name") if audio else None})

        cmd(["ffmpeg", "-v", "error", "-xerror", "-i", str(candidate), "-f", "null", "-"])
        check("full_decode", True, "Every video and audio frame decoded without errors")

        for name, spec in config.get("source_files", {}).items():
            file = locate(spec["path"])
            actual = sha256(file)
            check("source_" + name, actual == spec["sha256"],
                  {"expected": spec["sha256"], "actual": actual, "file": str(file)})

        if config.get("audio_reference"):
            def encoded_audio(path):
                stream = cmd(["ffmpeg", "-v", "error", "-i", str(path), "-map", "0:a:0", "-c:a", "copy", "-f", "adts", "pipe:1"])
                return hashlib.sha256(stream).hexdigest()
            actual = encoded_audio(candidate)
            expected = encoded_audio(locate(config["audio_reference"]))
            check("audio_unchanged", actual == expected, {"candidate_adts_sha256": actual, "reference_adts_sha256": expected})

        if config.get("subtitles"):
            captions = srt_text(locate(config["subtitles"]))
            check("captions_text_file", len(captions) == config.get("caption_count", len(captions))
                  and "、" not in "".join(captions), {"cue_count": len(captions), "burn_in_not_verified": True})
            if config.get("locked_script"):
                locked = locate(config["locked_script"]).read_text(encoding="utf-8")
                if "## 音声台本（LOCK）" in locked:
                    locked = locked.split("## 音声台本（LOCK）", 1)[1].split("## 制作上の留意点", 1)[0].strip()
                check("caption_matches_lock", normalize("".join(captions)) == normalize(locked),
                      {"caption_characters": len(normalize("".join(captions))),
                       "locked_characters": len(normalize(locked))})

        for scene in config.get("motion_windows", []):
            measured = motion_diff(candidate, scene["start"], scene["end"], scene["crop"])
            observations[scene["name"]] = {"value": measured, "times": [scene["start"], scene["end"]],
                                            "roi": scene["crop"], "not_a_quality_score": True}
            if "min_motion" in scene:
                check("planned_motion_" + scene["name"], measured >= scene["min_motion"],
                      {"value": measured, "expected_minimum_for_this_scene_only": scene["min_motion"]})
    except Exception as exc:
        checks["execution"] = {"status": "FAIL", "detail": str(exc)}

    automatic_pass = bool(checks) and all(c["status"] == "PASS" for c in checks.values())
    result = {
        "candidate": str(candidate),
        "automatic_checks": checks,
        "automatic_pass": automatic_pass,
        "motion_observations": observations,
        "review_gates": {
            "real_time_visual_and_audio_review": "NOT_REVIEWED",
            "visual_clarity_and_aesthetic_quality": "NOT_REVIEWED",
            "presenter_role": "NOT_REVIEWED",
            "original_repository_preflight_and_tests": "NOT_REVIEWED",
            "external_g2_g3": "NOT_REVIEWED"
        },
        "overall_status": "HOLD",
        "note": "Automatic PASS does not imply final or artistic PASS; subtitle file checks do not verify on-screen rendering."
    }
    out = Path(opts.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"automatic_pass": automatic_pass, "overall_status": "HOLD",
                      "checks": {key: value["status"] for key, value in checks.items()}},
                     ensure_ascii=False))
    return 0 if automatic_pass else 2


if __name__ == "__main__":
    sys.exit(main())
