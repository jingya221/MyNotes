# ADPRRT数据集生成规则文档

## 功能概述

`gen_adprrt`函数的主要功能是根据原始EDC数据和规范(spec)生成ADPR_RT(Analysis Data Procedures for Radiotherapy，分析用途的放疗程序数据集)数据集。这个数据集包含临床试验中各受试者的放射治疗相关信息，如放疗部位、剂量、适应症和治疗日期等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADPR_RT相关的JSON规范列表
- `cutoffdate`: 主要的数据截止日期

## 输入和输出

- **输入**: 原始EDC数据和JSON规范
- **输出**: 包含规范中要求的所有变量的ADPR_RT数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 使用simple_adam_gen函数从原始数据中生成基础数据集
3. 设置PRTRT变量固定为"Radiotherapy"
4. 根据截止日期处理数据
5. 返回最终的ADPRRT数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从PRRT.STUDYCODE或PRRT.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从PRRT.SUBJID获取 |

### 治疗信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PRTRT | 报告的程序名称 | 固定值："Radiotherapy" |
| PRCAT | 类别 | 从PRRT.TNAME获取 |
| PRINDC | 适应症 | 从PRRT.PRINDC获取 |
| PRINDCO | 其他适应症，请具体说明 | 从PRRT.PRINDCO获取 |
| PRLOC | 部位 | 从PRRT.PRLOC获取 |
| PRLOCO | 其他部位，请具体说明 | 从PRRT.PRLOCO获取 |

### 日期变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PRSTDTC | 观察开始日期/时间 | 从PRRT.PRSTDAT获取 |
| PRENDTC | 观察结束日期/时间 | 从PRRT.PRENDAT获取 |

### 剂量和评估变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PRDOSTXT | 剂量描述 | 从PRRT.PRDOSE获取 |
| PRDOSU | 剂量单位 | 从PRRT.PRDOSU获取 |
| PRTORRES | 放疗后的反应评估 | 从PRRT.PRORRES获取 |

## 数据截取处理

根据传入的cutoffdate参数，对ADPRRT数据进行如下处理：

1. 过滤掉PRSTDTC > cutoffdate的记录
2. 当PRENDTC > cutoffdate时，将PRENDTC设置为空值(NA)

## 代码限制和注意事项

1. 函数依赖于特定的数据结构和变量命名规则
2. 函数使用simple_adam_gen辅助函数来生成基础数据集，这可能导致对该辅助函数的依赖
3. PRTRT变量在代码中被硬编码为固定值"Radiotherapy"，与规范文件的描述一致