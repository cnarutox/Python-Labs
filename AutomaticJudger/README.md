
    参考答案.docx 与 成绩单.xls 需要同该 judge.py 文件位于同一目录下;
    答题卡都应位于 答题卡文件夹 中, 此文件夹也应同 judge.py 文件位于同一目录:
    │  judge.py
    │  参考答案.docx
    │  成绩单.xls
    └──答题卡
            1-罗.docx
            2-段.docx
            3-曾.docx
            4-朱.docx
            5-赵.docx

- 基于Python读取word标准答案并自动判分，答案填充在Excel中，代码简练50行，可扩展性中上
1. 读取某个文件夹下的word文件
   
   安装python-docx模块

   from docx import Document

   document=Document(path) #读取word内容

2. 读取参考答案内容 

   paragraph=document.paragraphs #获取word中的每个段落

   parstr=paragraph.text #获取段落中的文本

3. 读取答题卡内容

   tables=document.tables #获取word中的表格

   tables1=tables[1] #获取第二个表格

   tables1.rows #获取表格行

   tables1.columns #获取表格列

   tables1.cell(i,j).text #获取表格第i行第j列数据

4. 对答题卡与参考答案中的内容进行比较，正确则加分，错误不加，最后得出每类大题的总分，并写入到word文件中

   table1.cell(i,j).text=str #修改word表格中的文本

   document.save(path) #保存word文档

5. 对于第50题翻译及最后一题作文题，判断是否为空，如果是，则判为零分；

   a. 第50题比较相似度，60%以上给满分7分，30-60%给6分

   import difflib #比较序列的标准库

   difflib.SequenceMatcher(None,str1,str2).ratio() #比较两个序列的相似度

   b. 作文题通过字数判断得分。 20-30词给6分， 30-40词给8分， 40-50词给10分， 50-60给12分，  60以上给13分；

6. 读取该word文件中各项大题的分数并相加，将最后总分写入成绩单中。

   import xlrd #导入excel模块

   import xlwt 

   rb=xlrd.open_workbook(path) #打开excel

   table=rb.sheets()[0] #读取表单

   table.nrows #获取表单行

   table.ncols #获取表单列

   from xlutils.copy import copy #导入excel复制模块

   wb = copy(rb) #复制表单

   ws=wb.get_sheet(0) #获取表单

   ws.write(i, j, value) #改变表单的值

   wb.save(path) #保存表单

7. 重复3-6。
