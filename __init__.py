import os
from aiohttp import web

from .remote_combo_native import RemoteComboNative
from .new_combo import NewCombo

WEB_DIRECTORY = "web"

async def list_folders(request):
    base  = request.query.get("folder", "") or "input"
    print("base path is: ", base);

    folder_list = [base.replace("\\", "/").lstrip("./")]
    for root, dirs, _ in os.walk(base):
        for d in dirs:
            full_path = os.path.join(root, d)
            try:
                rel_path = os.path.relpath(full_path, ".")
            except ValueError:
                rel_path = full_path
            folder_list.append(rel_path.replace("\\", "/"))

    return web.json_response(folder_list);
    return web.json_response({"folders": folder_list})


# Register the routes
try:
    from server import PromptServer
    PromptServer.instance.app.router.add_get(
        "/remote-combo-demo/list_folders", list_folders
    )
except Exception as e:
    print("Could not register /list_files route:", e)

NODE_CLASS_MAPPINGS = {
    "RemoteComboNative": RemoteComboNative,
    "NewCombo" : NewCombo,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RemoteComboNative": "Remote Combo Native",
    "NewCombo" : "New Combo",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]