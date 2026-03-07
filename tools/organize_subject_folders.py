# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = ROOT / "curriculum_index.csv"

SUBJECT_FOLDER_MAP = {
    "Python 프로그래밍": "pyBasics",
    "Python 전처리 및 시각화": "dataVizPrep",
    "머신러닝과 딥러닝": "mlDeepDive",
    "자연어 및 음성 데이터 활용 및 모델 개발": "nlpSpeechAI",
    "음성 데이터 활용한 TTS와 STT 모델 개발": "speechTtsStt",
    "거대 언어 모델을 활용한 자연어 생성": "llmTextGen",
    "프롬프트 엔지니어링": "promptEng",
    "Langchain 활용하기": "langChainLab",
    "RAG(Retrieval-Augmented Generation)": "ragPipeline",
}


def read_index() -> tuple[list[str], list[str], list[dict[str, str]]]:
    with INDEX_FILE.open(encoding="utf-8-sig", newline="") as fp:
        all_lines = fp.readlines()

    comments: list[str] = []
    data_lines: list[str] = []
    for line in all_lines:
        if line.strip() and line.lstrip().startswith("#"):
            comments.append(line.rstrip("\n"))
            continue
        if line.strip():
            data_lines.append(line)

    reader = csv.DictReader(data_lines)
    raw_fieldnames = reader.fieldnames or []
    fieldnames = [str(name).lstrip("\ufeff") for name in raw_fieldnames]
    rows: list[dict[str, str]] = []
    for raw in reader:
        rows.append({str(key).lstrip("\ufeff"): value for key, value in raw.items()})
    return comments, fieldnames, rows


def write_index(comments: list[str], fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with INDEX_FILE.open("w", encoding="utf-8", newline="\n") as fp:
        for comment in comments:
            fp.write(comment + "\n")
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resolve_existing_class_dir(class_id: str, old_md_file: str, target_dir: Path) -> Path | None:
    candidates: list[Path] = []

    old_md = old_md_file.strip()
    if old_md:
        old_parent = (ROOT / Path(old_md)).parent
        if old_parent.name == class_id:
            candidates.append(old_parent)

    candidates.append(ROOT / class_id)
    for folder in SUBJECT_FOLDER_MAP.values():
        candidates.append(ROOT / folder / class_id)

    for candidate in candidates:
        if candidate == target_dir:
            continue
        if candidate.exists() and candidate.is_dir():
            return candidate
    return None


def organize_subject_folders() -> None:
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"Cannot find index file: {INDEX_FILE}")

    comments, fieldnames, rows = read_index()

    unknown_subjects = sorted({row["subject_name"] for row in rows if row["subject_name"] not in SUBJECT_FOLDER_MAP})
    if unknown_subjects:
        raise ValueError(f"Unknown subjects in index: {unknown_subjects}")

    moved = 0
    already = 0
    missing = 0

    seen_class_ids: set[str] = set()
    for row in rows:
        class_id = row["class"].strip()
        if not class_id or class_id in seen_class_ids:
            continue
        seen_class_ids.add(class_id)

        subject_name = row["subject_name"]
        folder_name = SUBJECT_FOLDER_MAP[subject_name]
        target_dir = ROOT / folder_name / class_id
        target_dir.parent.mkdir(parents=True, exist_ok=True)

        if target_dir.exists():
            already += 1
            continue

        src_dir = resolve_existing_class_dir(class_id, row.get("md_file", ""), target_dir)
        if src_dir is None:
            missing += 1
            continue

        shutil.move(str(src_dir), str(target_dir))
        moved += 1

    for row in rows:
        class_id = row["class"].strip()
        folder_name = SUBJECT_FOLDER_MAP[row["subject_name"]]
        row["md_file"] = f"{folder_name}/{class_id}/{class_id}.md"

    write_index(comments, fieldnames, rows)

    print(f"Moved class dirs: {moved}")
    print(f"Already organized: {already}")
    print(f"Missing class dirs: {missing}")
    print(f"Updated index rows: {len(rows)}")


if __name__ == "__main__":
    organize_subject_folders()
