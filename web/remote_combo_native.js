import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "remote_combo_native",

    setup() 
	{	
        const graph = app.graph;
        const originalAdd = graph.add;
		
        graph.add = function (...args) 
		{
            const node = originalAdd.apply(this, args);
			
            if (node?.comfyClass !== "RemoteComboNative") 
			{
				return node;
			}

            const widgets = node.widgets || [];
            const baseDirWidget = widgets.find(w => w.name === "base_dir");
            const folderWidget = widgets.find(w => w.name === "folder");

            if (!baseDirWidget || !folderWidget) 
			{
                console.warn("[RemoteComboNative] Missing widgets");
                return node;
            }
			
            // Wire callback when base_dir changes
            baseDirWidget.callback = () => {
                const baseDir = baseDirWidget.value;
                refreshFolders(baseDir, folderWidget);
            };

            // Initial refresh (for hydration)
            setTimeout(() => 
			{
                refreshFolders(baseDirWidget.value, folderWidget);
            }, 50);

            return node;
        };
    }
});

/**
 * Updates the folder combo box with subfolders of the given base path.
 * @param {string} baseDir - The base directory to scan.
 * @param {Object} comboWidget - The folder combo box widget.
 */
function refreshFolders(baseDir, comboWidget) 
{
    fetch(`/remote-combo-demo/list_folders?folder=${encodeURIComponent(baseDir)}`)
        .then(res => res.json())
        .then(json => 
		{
            // Handle both raw array and wrapped dict
            const folders = Array.isArray(json) ? json : json?.folders || [];

            if (comboWidget.type === "combo") 
			{		
                comboWidget.options.values = { folders };
                comboWidget.value = folders[0] || "";
                comboWidget.options.forceInput = true;			
            }
        })
        .catch(err => {
            console.error("[RemoteComboNative] Failed to fetch folders:", err);
        });
}