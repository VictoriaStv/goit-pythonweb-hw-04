import asyncio
import aiofiles
import aiofiles.os
import argparse
import logging
from pathlib import Path
import shutil
import os

# логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_sorter.log"),
        logging.StreamHandler()
    ]
)

# Парсер
parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
parser.add_argument("source", type=str, help="Шлях до вихідної папки")
parser.add_argument("destination", type=str, help="Шлях до цільової папки")
args = parser.parse_args()

source_dir = Path(args.source)
destination_dir = Path(args.destination)

# Копіювання файлу
async def copy_file(file_path: Path):
    try:
        ext = file_path.suffix.lower().strip(".") or "no_extension"
        target_folder = destination_dir / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        target_path = target_folder / file_path.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_path)
        logging.info(f"✅ Скопійовано: {file_path} → {target_path}")

    except Exception as e:
        logging.error(f"❌ Помилка копіювання {file_path}: {e}")


async def read_folder(folder: Path):
    tasks = []

    try:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = Path(root) / file
                tasks.append(copy_file(full_path))

        await asyncio.gather(*tasks)

    except Exception as e:
        logging.error(f"❌ Помилка читання папки {folder}: {e}")

# точка входу
if __name__ == "__main__":
    if not source_dir.exists() or not source_dir.is_dir():
        logging.error(f"❌ Вихідна папка не існує або не є директорією: {source_dir}")
        exit(1)

    if not destination_dir.exists():
        destination_dir.mkdir(parents=True, exist_ok=True)
        logging.info(f"📁 Створено цільову папку: {destination_dir}")

    asyncio.run(read_folder(source_dir))
