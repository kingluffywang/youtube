# youtube
YouTube video processing scripts

## Update: Gradio interface intragration and auto installation

集成了Gradio WebUI界面。简化了安装步骤。支持拖拽操作。开箱即用。

1. 首先确保安装了 Python（新安装推荐 3.11.11 或更高版本）

2. 确保安装ffmpeg （支持mp3处理）：
需要手动安装

```bash
# Windows: 
# 下载 ffmpeg: https://www.gyan.dev/ffmpeg/builds/
# 添加到系统环境变量（具体参阅 ffmpeg 安装文档）

# Linux:
sudo apt-get install ffmpeg
# Mac:
brew install ffmpeg
```

3. git clone 本仓库

```bash
git clone https://... #本仓库地址#
```

3. 创建并激活虚拟环境（推荐）：
```bash
# 进入项目目录
cd youtube # 或自定义目录

# 创建虚拟环境
python3 -m venv venv
```

### 运行 WebUI

6. 运行脚本：

```bash
# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 运行脚本
python3 webui.py
```

### 说明
windows下可以直接双击start_windows.bat运行。
linux或者mac下也可以运行start.sh
`chmod +x your_script.sh` 赋予脚本可执行权限
`./start.sh`

脚本运行后，开浏览器访问 http://localhost:7860，进入 WebUI 界面。
输出路径统一在output文件夹下。



## 原脚本详解（使用WebUI的可略过）：

## 脚本 1: CN_mp3_audio2text.py

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
1. 首先确保安装了 Python（推荐 3.8 或更高版本）

2. 创建并激活虚拟环境（推荐）：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
3. 安装所需依赖：
```bash
# 安装基础依赖
pip install faster-whisper
pip install pydub
pip install numpy

# 如果处理 MP3 文件，还需要安装 ffmpeg
# Windows: 
# 下载 ffmpeg: https://www.gyan.dev/ffmpeg/builds/
# 添加到系统环境变量

# Linux:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```
**使用示例：**
```python
# 导入函数
from your_script import transcribe_audio

# 调用函数进行转录
result = transcribe_audio(
    audio_file_path="你的音频文件.mp3",
    output_file_path="输出文本.txt",
    language="zh"  # 支持的语言代码，如 zh=中文, en=英文
)
```
**注意事项：**
1. 代码使用 CPU 进行计算（`device="cpu"`），如果有 GPU 可以修改为 `device="cuda"`
2. 使用了 `large-v2` 模型，需要较大内存，如果内存不足可以换用较小的模型
3. 使用了 `int8` 量化（`compute_type="int8"`）来减少内存占用
4. 程序会显示详细的处理进度，方便监控长音频的转录进度

## 脚本 2： zimu.py
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

1. 确保安装了 Python（推荐 3.8 或更高版本）

2. 创建并激活虚拟环境（推荐）：
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. 安装所需依赖：
```bash
# 安装基础依赖
pip install faster-whisper
pip install pydub
pip install numpy

# 安装 ffmpeg（处理音频文件必需）
# Windows: 
# 1. 下载 ffmpeg: https://www.gyan.dev/ffmpeg/builds/
# 2. 解压并添加到系统环境变量

# Linux:
sudo apt-get install ffmpeg

# Mac:
brew install ffmpeg
```

**使用示例：**
```python
# 导入函数
from your_script import transcribe_audio_to_srt

# 调用函数生成字幕
result = transcribe_audio_to_srt(
    audio_file_path="你的音频.mp3",
    output_srt_path="输出字幕.srt",
    language="zh"  # 支持的语言代码，如 zh=中文, en=英文
)
```

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
1. 代码使用 CPU 进行计算，可通过修改 `device="cuda"` 启用 GPU 加速
2. 使用了 `large-v2` 模型，需要较大内存，可以根据需要选择较小的模型
3. 使用了 `int8` 量化以减少内存占用
4. 输出的 SRT 文件采用 UTF-8 编码，兼容大多数播放器
5. 程序会显示详细的处理进度，方便监控长音频的转录进度



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
```



## 脚本 2-b 音频转字幕工具说明文档：zimu_jianti.py 生成简体字的字幕

## 功能简介

这是一个基于 Faster Whisper 的音频转写工具，可以将音频文件转换为带时间戳的 SRT 格式字幕文件。主要特点：

- 支持多种音频格式转换为 SRT 字幕
- 支持中文语音识别
- 支持繁体转简体中文
- 提供详细的转换进度提示
- 使用 Whisper large-v3 模型保证准确率

## 环境要求

使用前需要安装以下 Python 包：

```bash
pip install faster-whisper
pip install pydub
pip install numpy
pip install opencc-python-reimplemented
```

## 使用方法

### 基础用法

```python
from audio_transcribe import transcribe_audio_to_srt

# 基本调用方式
transcribe_audio_to_srt(
    audio_file_path="input.mp3",    # 输入音频文件路径
    output_srt_path="output.srt",   # 输出字幕文件路径
    language="zh",                  # 音频语言（默认中文）
    to_simplified=True              # 是否转换为简体中文
)
```

### 参数说明

- `audio_file_path`：输入音频文件路径，支持多种格式（mp3、wav 等）
- `output_srt_path`：输出 SRT 字幕文件的保存路径
- `language`：音频语言代码，默认为 "zh"（中文）
- `to_simplified`：是否将输出转换为简体中文，默认为 True

## 功能详解

1. **音频预处理**
   - 自动将音频转换为单声道
   - 采样率设置为 16kHz
   - 支持多种音频格式输入

2. **语音识别优化**
   - 使用 large-v3 模型提高识别准确率
   - 启用语音活动检测（VAD）
   - 配置上下文关联以提高准确性
   - 通过参数配置减少随机性

3. **字幕生成**
   - 自动生成序号编号
   - 精确的时间戳标记
   - 支持繁简中文转换
   - 标准 SRT 格式输出

## 输出示例

```
1
00:00:00,000 --> 00:00:02,500
这是第一句话的内容

2
00:00:02,500 --> 00:00:05,000
这是第二句话的内容
```

## 进度显示

脚本执行过程中会显示详细的进度信息：

- 音频文件加载进度
- 模型加载状态
- 转录进度和时间戳
- 总体处理时间统计

## 注意事项

1. 首次运行时会自动下载 Whisper 模型，需要稳定的网络连接
2. 处理长音频文件时可能需要较长时间
3. 建议使用高质量的音频输入以获得更好的识别效果
4. 确保系统有足够的存储空间和内存

## 错误处理

如果遇到问题，请检查：

- 所有依赖包是否正确安装
- 输入音频文件是否存在且格式正确
- 系统是否有足够的存储空间
- 网络连接是否正常（首次运行需要下载模型）



## Video Processing

## 脚本 5： video-resize.py

**代码功能概述：**
这是一个视频分辨率转换工具，专门用于将普通视频转换为适合 YouTube Shorts 的垂直视频格式（1080x1920）。主要功能：
1. 自动创建输出目录（如果不存在）
2. 调整视频分辨率到 1080x1920
3. 保持原始视频的宽高比
4. 用黑边填充空白区域（居中处理）
5. 保持原始音频质量不变

**安装步骤：**

1. 确保安装了 Python（推荐 3.6 或更高版本）

2. 安装 FFmpeg
```bash
# Windows:
# 1. 下载 FFmpeg: https://www.gyan.dev/ffmpeg/builds/
# 2. 解压并将 bin 目录添加到系统环境变量

# Linux:
sudo apt update
sudo apt install ffmpeg

# Mac:
brew install ffmpeg
```

3. 验证安装
```bash
# 在终端/命令行中验证 FFmpeg 是否安装成功
ffmpeg -version
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
- `input_file`: 输入视频文件路径
- `output_file`: 输出视频文件路径
- 输出视频尺寸: 1080x1920 像素（适合 YouTube Shorts）
- 处理方式：
  - 保持原始视频比例
  - 自动添加黑边填充
  - 视频居中显示
  - 保持原始音频质量

**注意事项：**
1. 确保系统已正确安装 FFmpeg 并添加到环境变量
2. 输入视频可以是任何 FFmpeg 支持的格式
3. 如果输出目录不存在，程序会自动创建
4. 代码会保持原始音频流（`-c:a copy`），这样可以加快处理速度
5. 如果转换过程出错，会打印详细的错误信息

**可能的报错处理：**
- 如果遇到 "FFmpeg not found" 错误，请检查 FFmpeg 是否正确安装并添加到环境变量
- 如果遇到权限错误，请确保对输出目录有写入权限
- 如果输入文件不存在，会提示相应的错误信息


## 脚本6 Video Splitter：general_shorts_cut.py 

一个简单但功能强大的视频分割工具，可以将长视频自动分割成59秒的短片段。这个工具特别适合需要将视频内容切分成短视频的场景，比如准备短视频平台的内容。

## 功能特点

- 自动将视频分割成59秒的片段
- 保持原视频的质量
- 自动创建输出目录
- 使用H.264视频编码和AAC音频编码
- 显示处理进度
- 自动对输出文件进行编号

## 环境要求

- Python 3.6+
- moviepy
- ffmpeg

## 安装步骤

1. 首先确保您的系统已安装Python 3.6或更高版本。

2. 安装必要的Python包：
```bash
pip install moviepy
```

3. 安装ffmpeg（moviepy的依赖）：

   - Windows用户：
     ```bash
     # 使用Chocolatey包管理器
     choco install ffmpeg
     ```
   
   - Mac用户：
     ```bash
     # 使用Homebrew包管理器
     brew install ffmpeg
     ```
   
   - Linux用户：
     ```bash
     # Ubuntu/Debian
     sudo apt-get install ffmpeg
     
     # CentOS
     sudo yum install ffmpeg
     ```

4. 下载项目文件：
```bash
git clone [你的项目地址]
cd video-splitter
```

## 使用方法

1. 打开`split_video.py`文件，修改以下参数：
```python
input_video = "你的视频文件路径.mp4"  # 修改为您的输入视频路径
output_folder = "输出文件夹路径"      # 修改为您想要保存分割视频的文件夹路径
```

2. 运行脚本：
```bash
python split_video.py
```

3. 等待处理完成，分割后的视频片段将保存在指定的输出文件夹中。

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

1. 如果遇到ffmpeg相关错误，请确保：
   - ffmpeg已正确安装
   - ffmpeg可以在命令行中访问（已添加到系统PATH）

2. 如果出现内存错误，可以尝试：
   - 关闭其他占用内存的程序
   - 处理较小的视频文件
   - 增加系统的虚拟内存