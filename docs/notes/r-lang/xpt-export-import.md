# XPT文件导出与读取

## 概述

XPT（SAS Transport）文件是一种用于在不同统计软件之间交换数据的标准格式。在R语言中，我们可以使用多个包来处理XPT文件。

## 主要R包

### 1. haven包
最推荐的现代化解决方案：

```r
# 安装
install.packages("haven")
library(haven)

# 读取XPT文件
data <- read_xpt("path/to/file.xpt")

# 写入XPT文件
write_xpt(data, "path/to/output.xpt")
```

### 2. SASxport包
传统解决方案：

```r
# 安装
install.packages("SASxport")
library(SASxport)

# 读取XPT文件
data <- read.xport("path/to/file.xpt")

# 写入XPT文件
write.xport(data, file = "path/to/output.xpt")
```

## 实用示例

### 读取和检查XPT文件

```r
library(haven)

# 读取文件
df <- read_xpt("example.xpt")

# 查看数据结构
str(df)
head(df)

# 检查变量标签和属性
attr(df, "label")
sapply(df, function(x) attr(x, "label"))
```

### 导出数据为XPT格式

```r
# 准备数据
data(mtcars)

# 添加变量标签（可选）
attr(mtcars$mpg, "label") <- "Miles per gallon"
attr(mtcars$hp, "label") <- "Horsepower"

# 导出为XPT文件
write_xpt(mtcars, "mtcars.xpt")
```

## 注意事项

!!! warning "兼容性"
    - XPT文件有变量名长度限制（8个字符）
    - 某些特殊字符可能不被支持
    - 日期时间格式需要特别处理

!!! tip "最佳实践"
    - 优先使用haven包，它更现代且维护活跃
    - 导出前检查变量名是否符合XPT规范
    - 备份原始数据以防格式转换丢失信息

## 常见问题

### 1. 中文字符处理
```r
# 设置编码
data <- read_xpt("file.xpt", encoding = "UTF-8")
```

### 2. 大文件处理
```r
# 分块读取（如果支持）
# 或者增加内存限制
memory.limit(size = 8000)  # Windows系统
```

### 3. 数据类型转换
```r
# 转换为适当的R数据类型
df$date_var <- as.Date(df$date_var)
df$factor_var <- as.factor(df$factor_var)
``` 