# jellyfin-retitle

This is a Python script for automatically renaming video files in a specific folder in the Jellyfin media server.

## How To Use

1. Install Docker (Compose)
2. Edit the ```.env``` file. (Copy from .env.example)
3. Execute ```docker-compose up``` (If as daemon, Add the ```-d``` option.)

## Parameter Description

The following are the parameters that can be defined and their purposes:

1. `USER_NAME`: Used to set the username for the Jellyfin media server. Must match an existing username on the Jellyfin server. **This parameter is required.**

2. `BASE_URI`: Used to set the base URI for the Jellyfin server. Typically "http://127.0.0.1:8096". If you are using a different URI, change this parameter accordingly. This parameter is required.

3. `API_TOKEN`: Used to set the Jellyfin API access token. Can be obtained in Jellyfin server under "Settings" > "API" > "API Key". **This parameter is required.**

4. `TITLE_TEMPLATE`: Used to set the new name for the video file, see **Title Template** section for details. This parameter is optional.

5. `SCAN_INTERVAL`: Scan interval in seconds. This parameter specifies the time the script waits after scanning the folder. Default value is 30 seconds. This parameter is optional.

When using this script, the above parameters must be set to the correct values and ensure that the Jellyfin server is running during the script's execution.

### Title Template

If this parameter is not set, the original name of the video file will be used. The following variables are available to use in the `TITLE_TEMPLATE` variable:

| Variable Name             | Description                     |
|---------------------------|---------------------------------|
| parent_id                 | ID of the parent folder of the video file |
| parent_name               | Name of the parent folder of the video file |
| item_id                   | ID of the video file             |
| item_path                 | Full path of the video file      |
| item_name                 | Original name of the video file  |
| item_index                | Index of the video file in the parent folder |
| item_filename             | Full filename of the video file  |
| item_ext                  | Extension of the video file      |
| item_filename_without_ext | Filename of the video file without extension |

To use these variables in the `TITLE_TEMPLATE` parameter, use Python string formatting syntax. For example, to create a new name using the `parent_name` and `item_index` variables, set `TITLE_TEMPLATE` as follows:

```
TITLE_TEMPLATE = '%(parent_name)s - %(item_index)s'
```

This will create a new name that includes the name of the parent folder and the index of the video file in the parent folder as the episode number. Different formatting strings can be used to create different new names as needed.

## Other Notes

The "scan" function in the script will scan all video files in the specified folder in the Jellyfin server and pass each file to the "callback" function for processing. In this script, the "callback" function is the "retitle" function, which will rename the video file.

The "retitle" function will check if the name of each video file needs to be changed. If it needs to be changed, it will create a new name using the template defined in the "TITLE_TEMPLATE" parameter and use the new name to update the video file name on the Jellyfin server. If the "TITLE_TEMPLATE" parameter is not set, the original name of the video file will be used.

The script will run continuously and wait for the time defined in the "SCAN_INTERVAL" parameter after each folder scan. To stop the script, press Ctrl+C.
