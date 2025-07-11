import { app } from "../../scripts/app.js";

app.registerExtension(
{
    name: "new_combo",
    setup() 
	{
        const graph = app.graph;
        const originalAdd = graph.add;

        graph.add = function (...args) 
		{
            const node = originalAdd.apply(this, args);

            if (node?.comfyClass === "NewCombo") 
			{
                const base = node.widgets?.find(w => w.name === "base_dir");
                const folder = node.widgets?.find(w => w.name === "folder");
                wireWidgets(base, folder);
            }

            return node;
        };
    }
});

function refreshFolders(basePath, comboWidget) 
{
    fetch(`/remote-combo-demo/list_folders?folder=${encodeURIComponent(basePath)}`)
        .then(res => res.json())
        .then(folders => 
		{
            if (Array.isArray(folders)) 
			{
                comboWidget.options.values = folders;
                comboWidget.value = basePath;
                comboWidget.options.forceInput = true;
            }
        })
        .catch(err => 
		{
            console.warn("Failed to fetch folders:", err);
        });
}

function wireWidgets(baseWidget, comboWidget) 
{
    if (!baseWidget || !comboWidget) 
	{
        console.warn("Missing base or combo widget");
        return;
    }

    baseWidget.callback = () => 
	{
        refreshFolders(baseWidget.value, comboWidget);
    };

    setTimeout(() => 
	{
        refreshFolders(baseWidget.value, comboWidget);
    }, 50);
}

