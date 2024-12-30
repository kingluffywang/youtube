# youtube
YouTube video processing scripts

脚本 1: CN_mp3_audio2text.py
这段代码的功能和安装步骤。

**代码功能概述：**
这是一个音频转文字的程序，主要功能是将 MP3 音频文件转换为文本。具体来说：
1. 加载 Whisper 大型语音识别模型
2. 读取并预处理 MP3 音频文件（转换为单声道、16kHz采样率）
3. 将音频数据转换为模型可处理的格式
4. 执行语音识别，生成文本
5. 将转录结果保存到文件
6. 提供详细的处理进度和时间统计

**安装步骤：**
1. 首先确保安装了 Docker

2. 镜像构建运行环境

```bash
docker build -t youtubeenv .
```

**使用示例：**

将需要处理的音频文件放置到脚本目录

```bash
# 导入函数
docker run -v $(pwd):/data --workdir /data youtubeenv CN_mp3_audio2text.py -i 你的音频文件.mp3 -o 输出文本.txt
```

可选参数
* --lang # 支持的语言代码，如 zh=中文, en=英文，默认 "zh"

**注意事项：**
1. 代码使用 CPU 进行计算（`device="cpu"`），如果有 GPU 可以修改为 `device="cuda"`，同时运行 `docker run` 注意时传递 `--gpus` 指定 GPU 卡数
2. 使用了 `large-v2` 模型，需要较大内存，如果内存不足可以换用较小的模型
3. 使用了 `int8` 量化（`compute_type="int8"`）来减少内存占用
4. 程序会显示详细的处理进度，方便监控长音频的转录进度

脚本 2： zimu.py
我来帮你总结这段代码的功能和安装步骤。

**代码功能概述：**
这是一个音频转字幕的程序，它可以将音频文件转换为标准的 SRT 格式字幕文件。主要功能包括：
1. 将音频时间点转换为 SRT 时间戳格式（如：00:00:03,456）
2. 加载 Whisper 语音识别模型
3. 处理和转换音频文件（转单声道、16kHz采样率）
4. 执行语音识别，获取带时间戳的文本片段
5. 生成标准 SRT 格式字幕文件（包含序号、时间轴、文本内容）
6. 提供详细的处理进度和时间统计

**安装步骤：**

1. 首先确保安装了 Docker

2. 镜像构建运行环境

```bash
docker build -t youtubeenv .
```

**使用示例：**

```bash
docker run -v $(pwd):/data --workdir /data youtubeenv zimu.py -i 你的音频.mp3 -o 输出字幕.srt
```

可选参数
* --lang # 支持的语言代码，如 zh=中文, en=英文，默认 "zh"

**生成的 SRT 格式示例：**
```
1
00:00:00,000 --> 00:00:02,500
第一段文字

2
00:00:02,500 --> 00:00:05,000
第二段文字
```

**注意事项：**
1. 代码使用 CPU 进行计算，可通过修改 `device="cuda"` 启用 GPU 加速，同时运行 `docker run` 注意时传递 `--gpus` 指定 GPU 卡数
2. 使用了 `large-v2` 模型，需要较大内存，可以根据需要选择较小的模型
3. 使用了 `int8` 量化以减少内存占用
4. 输出的 SRT 文件采用 UTF-8 编码，兼容大多数播放器
5. 程序会显示详细的处理进度，方便监控长音频的转录进度

脚本 3： video-resize.py

**代码功能概述：**
这是一个视频分辨率转换工具，专门用于将普通视频转换为适合 YouTube Shorts 的垂直视频格式（1080x1920）。主要功能：
1. 自动创建输出目录（如果不存在）
2. 调整视频分辨率到 1080x1920
3. 保持原始视频的宽高比
4. 用黑边填充空白区域（居中处理）
5. 保持原始音频质量不变

**安装步骤：**

1. 首先确保安装了 Docker

2. 镜像构建运行环境

```bash
docker build -t youtubeenv .
```

**使用示例：**
```python
# 导入函数
from video_converter import resize_video_for_youtube_shorts

# 转换视频
resize_video_for_youtube_shorts(
    input_file="原始视频.mp4",
    output_file="shorts版本.mp4"
)
```

**参数说明：**
- `-i` 或者 `--input`: 输入视频文件路径
- `-o` 或者 `--output`: 输出视频文件路径
- 输出视频尺寸: 1080x1920 像素（适合 YouTube Shorts）
- 处理方式：
  - 保持原始视频比例
  - 自动添加黑边填充
  - 视频居中显示
  - 保持原始音频质量

脚本 4： helper_srt_spacerm.py
让我来总结这个字幕处理工具的功能和使用方法。

**功能概述：**
这是一个字幕文本处理工具，主要用于：
1. 删除字幕文件中的所有空格（包括半角和全角空格）
2. 删除所有换行符和回车符
3. 将所有文本内容合并为单行输出
4. 删除所有空白行
5. 保持 UTF-8 编码

**使用方法：**

1. 安装要求：
```bash
# 只需要 Python 3.x 版本，不需要额外安装任何库
python --version  # 检查 Python 版本
```

2. 代码使用：
```python
# 方法一：直接运行脚本
python script.py  # 脚本会处理默认的 '音频字幕.srt' 文件

# 方法二：在其他代码中导入使用
from script import remove_spaces_newlines

# 处理自定义文件
remove_spaces_newlines(
    input_file='你的字幕文件.srt',  
    output_file='输出文件.srt'
)
```

**注意事项：**
1. 处理前建议备份原始文件，因为处理后将丢失原有格式
2. 确保输入文件为 UTF-8 编码
3. 输出文件会自动以 UTF-8 编码保存
4. 处理后的文件会失去原有的换行和格式，全部内容将在一行显示
5. 如果输出文件已存在，会被覆盖

**适用场景：**
- 需要对字幕文本进行文本分析时
- 需要提取纯文本内容时
- 需要合并多行文本为单行时
- 处理含有多余空格的字幕文件时

**输入输出示例：**
```
输入文件内容：
这是第一行   内容
这是第二行 内容
  这是第三行

输出文件内容：
这是第一行内容这是第二行内容这是第三行
脚本5：general_shorts_cut.py
# Video Splitter

一个简单但功能强大的视频分割工具，可以将长视频自动分割成59秒的短片段。这个工具特别适合需要将视频内容切分成短视频的场景，比如准备短视频平台的内容。

## 功能特点

- 自动将视频分割成59秒的片段
- 保持原视频的质量
- 自动创建输出目录
- 使用H.264视频编码和AAC音频编码
- 显示处理进度
- 自动对输出文件进行编号

## 安装步骤

1. 首先确保安装了 Docker

2. 镜像构建运行环境

```bash
docker build -t youtubeenv .
```

## 使用方法

```bash
docker run -v $(pwd):/data --workdir /data youtubeenv general_shorts_cut.py -i 你的视频文件路径.mp4 -o /data
```

等待处理完成，分割后的视频片段将保存在当前目录中。

也可以指定其他目录

```bash
docker run -v $(pwd):/data -v /other/dir:/other/dir --workdir /data youtubeenv general_shorts_cut.py -i 你的视频文件路径.mp4 -o /other/dir
```

等待处理完成，分割后的视频片段将保存在目录 /other/dir 中。

## 输出格式

- 输出的视频文件将按照 `clip_001.mp4`, `clip_002.mp4`, ... 的格式命名
- 每个片段最长59秒
- 视频编码：H.264
- 音频编码：AAC

## 注意事项

- 确保有足够的磁盘空间存储分割后的视频片段
- 处理大型视频文件时可能需要较长时间
- 建议在处理重要视频前先备份原始文件
- 确保对输入视频文件和输出目录有正确的读写权限

## 常见问题解决

1. 如果出现内存错误，可以尝试：
   - 处理较小的视频文件
   - 关闭其他占用内存的程序、增加系统的虚拟内存，然后给容器更多内存 `docker run -m 16Gi ...`