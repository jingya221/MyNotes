# 05-ADPRTSURG数据集生成规则文档 

## 功能概述

`gen_adprtsurg`函数的主要功能是根据原始EDC数据和规范(spec)生成ADPR_TSURG(Analysis Data Procedures for Tumor Surgery，分析用途的肿瘤外科手术数据集)数据集。这个数据集包含临床试验中各受试者的肿瘤相关外科手术信息，如手术名称、类别、手术部位和手术日期等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADPR_TSURG相关的JSON规范列表
- `cutoffdate`: 主要的数据截止日期

## 输入和输出

- **输入**: 原始EDC数据和JSON规范
- **输出**: 包含规范中要求的所有变量的ADPR_TSURG数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 使用simple_adam_gen函数从原始数据中生成基础数据集
3. 根据截止日期处理数据
4. 返回最终的ADPRTSURG数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从PRTSURG.STUDYCODE或PRTSURG.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从PRTSURG.SUBJID获取 |

### 手术信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PRTRT | 报告的程序名称 | 从PRTSURG.PRTRT获取 |
| PRCAT | 类别 | 从PRTSURG.TNAME获取 |
| PRINDC | 适应症 | 从PRTSURG.PRINDC获取 |
| PRINDCO | 其他适应症，请具体说明 | 从PRTSURG.PRINDCO获取 |
| PRLOC | 部位 | 从PRTSURG.PRLOC获取 |
| PRLOCO | 其他部位，请具体说明 | 从PRTSURG.PRLOCO获取 |

### 日期变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PRSTDTC | 观察开始日期/时间 | 从PRTSURG.PRSTDAT获取 |

## 数据截取处理

根据传入的cutoffdate参数，对ADPRTSURG数据进行如下处理：

1. 过滤掉PRSTDTC > cutoffdate的记录

注意：与ADPRRT和ADPRLT不同，此函数不处理结束日期(PRENDTC)，因为在规范文件中没有定义这个变量。

## 代码限制和注意事项

1. 函数依赖于特定的数据结构和变量命名规则
2. 函数使用simple_adam_gen辅助函数来生成基础数据集，这可能导致对该辅助函数的依赖