# -*- coding: utf-8 -*-

def remove_spaces_newlines(input_file, output_file):
   """
   读取字幕文件，删除所有的空格和换行符，并将结果写为单行输出。
   
   功能:
   - 删除全角和半角空格
   - 删除所有换行符(\n)和回车符(\r) 
   - 删除空白行
   - 将处理后的内容写入单行
   
   参数:
       input_file (str): 输入字幕文件的路径
       output_file (str): 输出字幕文件的路径
       
   注意:
   - 文件使用UTF-8编码读写
   - 建议在处理前备份原始文件
   - 处理后的文件将失去原有的格式
   """
   
   # 以UTF-8编码打开输入文件
   with open(input_file, 'r', encoding='utf-8') as f_in:
       # 读取整个文件内容到内存
       content = f_in.read()
       
       # 移除半角空格和全角空格
       content = content.replace(' ', '')  # 移除半角空格
       content = content.replace('　', '')  # 移除全角空格
       
       # 移除所有换行符和回车符
       content = content.replace('\n', '')  # 移除换行符
       content = content.replace('\r', '')  # 移除回车符
       
   # 以UTF-8编码写入输出文件
   with open(output_file, 'w', encoding='utf-8') as f_out:
       # 将处理后的内容写入单行
       f_out.write(content)

if __name__ == '__main__':
   # 定义输入和输出文件路径
   input_srt = '音频字幕.srt'      # 原始字幕文件
   output_srt = '音频字幕_nos.srt'  # 处理后的文件
   
   # 调用函数处理文件
   remove_spaces_newlines(input_srt, output_srt)
   
   # 打印完成提示
   print("已删除所有空格和回车换行，生成文件：", output_srt)
