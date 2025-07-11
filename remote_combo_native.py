import os


class RemoteComboNative:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_dir": ("STRING", {"default": "input"}),
                "folder": ("COMBO", {
                    "base_dir" : "input",
                    "remote": {
                        "route": "/remote-combo-demo/list_folders",
                        "refresh_button": True,
                        "control_after_refresh": "first"
                    }
                }),
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
