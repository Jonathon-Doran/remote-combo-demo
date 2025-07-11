# remote-combo-demo

A minimal test suite demonstrating how remote `COMBO` inputs behave in ComfyUI, both **with** and **without** `force_input`.

This repo is intended for developers and node authors exploring dynamic UI behavior in ComfyUI — specifically the differences in how `COMBO` widgets can be updated at runtime via JavaScript and server endpoints.

## Overview

This demo includes:

- A working HTTP endpoint (`/remote-combo-demo/list_folders`) to list subdirectories
- Two custom nodes:
  - One using a `COMBO` input **without** `force_input`
  - One using a `COMBO` input **with** `force_input`
- A frontend JavaScript extension that wires the widgets and triggers live folder updates

## Nodes

### RemoteComboNative

Demonstrates a `COMBO` input populated remotely **without** `force_input`.

- Users must choose from the dropdown — custom input is disabled
- Useful for controlled, fixed-option environments
- Purpose: show how the lack of `force_input` affects flexibility

### MinimalFolderPicker

Demonstrates the same dynamic folder loading, but **with** `force_input: true`.

- Users can select from the list or type a custom folder path
- Purpose: showcase how dynamic `COMBO` inputs can support custom values with remote population

**Inputs (MinimalFolderPicker):**

- `base_dir` — root folder to scan for subfolders
- `folder` — a combo box that populates with subdirectories of `base_dir`

**Output:**

- Newline-separated string of files found in the selected folder

## How It Works

1. JavaScript extension watches for nodes of type `MinimalFolderPicker` or `RemoteComboNative`
2. When `base_dir` changes, it sends a request to:    
   ```
   GET /remote-combo-demo/list_folders?folder=<base_dir>
   ```
3. Server returns a list of subdirectories, which populates the `folder` combo box

> The `force_input: true` setting on the `folder` widget enables users to input paths not present in the list — critical for dynamic UIs.

## Installation

1. Clone into your `ComfyUI/custom_nodes/` directory:

```
       git clone https://github.com/Jonathon-Doran/remote-combo-demo.git
```

2. Restart ComfyUI

3. Look for nodes under remote-combo-demo category:

- Remote Combo Native
- New Combo

## License
MIT — use, fork, modify freely.