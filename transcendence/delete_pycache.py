import os
import shutil

def delete_pycache(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                print(f"Deleting {pycache_path}")
                shutil.rmtree(pycache_path)
        for file_name in files:
            if file_name.endswith(".pyc") or file_name.endswith(".pyo"):
                file_path = os.path.join(root, file_name)
                print(f"Deleting {file_path}")
                os.remove(file_path)

# 프로젝트의 루트 디렉토리 경로로 바꿔주세요.
project_root = '/Users/kyjo/goinfre/game'

delete_pycache(project_root)
print("All __pycache__ directories and .pyc files deleted.")
