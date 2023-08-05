# jellyfin-retitle

这是一个用于自动重命名 Jellyfin 媒体服务器中特定文件夹中的视频文件的 Python 脚本。

## 如何使用

1. 安装 Docker（包括 Docker Compose）。
2. 复制 ```.env.example``` 文件并将其命名为 ```.env```，然后进行编辑。
3. 执行 ```docker-compose up``` 命令来启动容器（如果要作为守护进程运行，则添加 ```-d``` 选项）。

## 参数说明

以下是可定义的参数及其用途：

1. `USER_NAME`：用于设置 Jellyfin 媒体服务器的用户名。必须与 Jellyfin 服务器上的现有用户名匹配。**此参数是必需的。**

2. `BASE_URI`：用于设置 Jellyfin 服务器的基本 URI。通常是 "http://127.0.0.1:8096"。如果您使用的是不同的 URI，请相应更改此参数。此参数是必需的。

3. `API_TOKEN`：用于设置 Jellyfin API 访问令牌。可以在 Jellyfin 服务器的“设置”>“API”>“API 密钥”中获取。**此参数是必需的。**

4. `TITLE_TEMPLATE`：用于设置视频文件的新名称，详情参考**标题模版**小节。此参数是可选的。

5. `SCAN_INTERVAL`：扫描间隔（以秒为单位）。此参数指定脚本在扫描完文件夹后等待的时间。默认值为 30 秒。此参数是可选的。

使用此脚本时，必须将上述参数设置为正确的值，并确保在脚本运行期间 Jellyfin 服务器处于运行状态。

### 标题模版

如果未设置此参数，则将使用视频文件的原始名称，下面是 `TITLE_TEMPLATE` 变量可用的变量：

| 变量名                       | 描述              |
|---------------------------|-----------------|
| parent_id                 | 视频文件父文件夹的 ID    |
| parent_name               | 视频文件父文件夹的名称     |
| item_id                   | 视频文件的 ID        |
| item_path                 | 视频文件的完整路径       |
| item_name                 | 视频文件的原始名称       |
| item_index                | 视频文件在父文件夹中的索引   |
| item_filename             | 视频文件的完整文件名      |
| item_ext                  | 视频文件的扩展名        |
| item_filename_without_ext | 视频文件的文件名（不带扩展名） |

要在 `TITLE_TEMPLATE` 参数中使用这些变量，请使用 Python 字符串格式化语法。例如，要使用 `parent_name` 和 `item_index`
变量创建新名称，可以参考以下内容设置`TITLE_TEMPLATE`。

```
TITLE_TEMPLATE = '%(parent_name)s - %(item_index)s'
```

此将创建一个新名称，其中包括父文件夹的名称和视频文件在父文件夹中的索引作为集数。根据需要，可以使用不同的格式化字符串来创建不同的新名称。

## 其它说明

脚本中的“scan”函数将扫描 Jellyfin 服务器中指定文件夹中的所有视频文件，并将每个文件传递给“callback”函数进行处理。在此脚本中，“callback”函数是“retitle”函数，它将重命名视频文件。

“retitle”函数将检查每个视频文件的名称是否需要更改。如果需要更改，将使用“TITLE_TEMPLATE”参数中定义的模板创建新名称，并将新名称用于更新
Jellyfin 服务器上的视频文件名称。如果未设置“TITLE_TEMPLATE”参数，则将使用原始视频文件名称。

脚本将一直运行，并在每次扫描文件夹后等待“SCAN_INTERVAL”参数中定义的时间。要停止脚本，请按 Ctrl+C。
