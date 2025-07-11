import os
from folder_paths import get_input_directory

class NewCombo:
    @classmethod
    def INPUT_TYPES(cls):
        input_dir = get_input_directory()
        rel_input = os.path.relpath(input_dir, ".").replace("\\", "/")

        return {
            "required": {
                "base_dir": ("STRING", {"default": rel_input}),
                "folder": ([rel_input], {"force_input": True, "label": "Subfolder"}),
            }
        }

    CATEGORY = "remote_combo_demo"
    FUNCTION = "list_files"
    OUTPUT_NODE = True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_list",)

    def list_files(self, base_dir, folder):
        try:
            path = folder.replace("/", os.sep)
            files = [
                f for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
            files.sort()
            result = "\n".join(files) if files else "(No files found)"
        except Exception as e:
            result = f"[ERROR] {e}"

        print(f"[DEBUG] Listing files in {path}:\n{result}")
        return (result,)
