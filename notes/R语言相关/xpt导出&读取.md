---
layout: default
title: xpt导出&读取
parent: R语言相关
nav_order: 1
---

# xpt导出&读取

在R和SAS之间进行数据交换时，XPT格式是一个重要的桥梁。本笔记记录了如何在R中导出XPT文件以及在SAS中读取的方法。

## R输出xpt

使用 `haven` 包可以轻松导出XPT格式文件：

```r
library(haven)
write_xpt(adam_data$ADAE, tmp, version = 5, name="ALL")
# version = 5 or 8
# name="ALL" 必须使用，否则R会自定义一个名字，导致读入SAS困难 
```

**参数说明**

- `version`: XPT文件版本，可选5或8
- `name`: 数据集名称，必须指定以确保SAS正确读取

## SAS读入xpt

在SAS中读取XPT文件的步骤：

```sas
libname xptin xport "C:\Users\wangjy35\Downloads\test\xpt\adae.xpt";
libname datasets 'C:\Users\wangjy35\Downloads\test\data';

proc copy in=xptin out=datasets;
run;
```

**操作流程**

1. 使用 `libname` 定义XPT文件路径
2. 定义目标数据集库  
3. 使用 `proc copy` 将数据复制到目标库

## 注意事项

- 确保文件路径正确
- XPT格式适用于FDA提交等场景
- 注意版本兼容性问题