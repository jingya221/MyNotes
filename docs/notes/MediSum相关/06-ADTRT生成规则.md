# ADTRT数据集生成规则文档

## 功能概述

`gen_adtrt`函数的主要功能是根据原始EDC数据和规范(spec)生成ADTRT(Analysis Data Tumor Response for Target Lesions，分析用途的靶病灶肿瘤反应数据集)数据集。这个数据集包含临床试验中各受试者靶病灶的测量信息，包括病灶直径、变化率和最佳反应等数据。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADTRT相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息
- `cutoffdate`: 主要的数据截止日期，默认为当前系统日期

## 输入和输出

- **输入**: 原始EDC数据、JSON规范和ADSL数据集
- **输出**: 包含规范中要求的所有变量的ADTRT数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 使用simple_adam_gen函数从原始数据中生成基础数据集
3. 提取靶病灶ID(TUID)，将相关数据集合并
4. 计算简单变量如TRLNKID、TRSTAT、PARAM、PARAMCD、ADT和AVAL
5. 根据截止日期过滤数据
6. 添加ADSL中的治疗开始日期，计算相对日期(ADY)
7. 标记基线记录(ABLFL)，计算基线值(BASE)和变化量(CHG、PCHG)
8. 计算病灶直径总和(Sum of Diameter)并计算最佳百分比变化标志(BPCHGFL)
9. 设置变量标签
10. 返回最终的ADTRT数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从TRT.STUDYCODE获取 |
| SUBJID | 研究中的受试者标识符 | 从TRT.SUBJID获取，作为合并变量1，用于匹配TU.SUBJID |
| TRREFID | 肿瘤成像ID | 从TRT.TULNKID获取，作为合并变量2，用于匹配TU.SN |
| TRLNKID | 链接ID | 将TRT.SN转换为'T'后跟两位数字格式 |

### 参数变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PARAM | 参数 | 固定值："Diameter (mm)", "Sum of Diameter(mm)" |
| PARAMCD | 参数代码 | 固定值："DIAMETER", "SUMDIAM" |

### 访视和评估变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AVISIT | 分析访视 | 从TRT.TRVISIT获取，作为合并变量3，用于匹配TU.TUVISIT |
| TRSTAT | 是否进行了评估 | 如果TRT.TRSTAT不等于"Yes"，则为"NOT DONE"，否则为空值(NA) |
| ADT | 分析日期 | 首先尝试从ymd(ADT)转换，如果为空值(NA)，则从TRREFID中提取日期部分 |
| ADY | 分析相对日 | 计算公式：<br>- 如果ADT >= TRTSDT，则ADY = ADT - TRTSDT + 1<br>- 如果ADT < TRTSDT，则ADY = ADT - TRTSDT |

### 测量值和变化量变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AVALC | 分析值(字符型) | 从TRT.TRLORRES获取 |
| TRORRESU | 原始单位 | 从TRT.TRORRESU获取 |
| AVAL | 分析值 | 将AVALC转换为数值型 |
| ABLFL | 基线记录标志 | 对于ADY <= 1的记录中，每个受试者-病灶组合中ADY最大的记录标记为"Y"，且仅对筛选访视的记录进行标记 |
| BASE | 基线值 | 取ABLFL="Y"的记录的AVAL值 |
| BASEC | 基线值(字符型) | 取ABLFL="Y"的记录的AVALC值 |
| CHG | 相对基线的变化 | 计算公式：AVAL - BASE |
| PCHG | 相对基线的百分比变化 | 计算公式：100 * (AVAL - BASE) / BASE |
| BPCHGFL | 最佳百分比变化标志 | 对于每个受试者，PCHG最小的记录标记为"Y" |

### 病灶位置和鉴别方法变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| TRLOC | 肿瘤/病灶的位置 | 从TRT.TULOC获取 |
| TRLOCDTL | 肿瘤/病灶位置的详细信息 | 从TRT.TULOCDTL获取 |
| TRMETHOD | 用于鉴别肿瘤的方法 | 从TU.TUMETHOD获取，通过匹配TRREFID中的病灶ID和AVISIT |
| TRMETOTH | 其他鉴别方法 | 从TU.TUMETHDO获取，通过匹配TRREFID中的病灶ID和AVISIT |
| TRSITEYN | 扫描是否在研究场所进行 | 从TU.TUSSYN获取，通过匹配TRREFID中的病灶ID和AVISIT |

### 病灶直径总和变量

函数还计算了"Sum of Diameter(mm)"参数，用于汇总每次访视的所有靶病灶测量值：

1. 对于基线记录：
   - 汇总每个受试者在基线访视的所有靶病灶直径
   - 设置PARAM为"Sum of Diameter(mm)"，PARAMCD为"SUMDIAM"

2. 对于基线后记录：
   - 汇总每个受试者在每次访视的所有靶病灶直径
   - 仅当当前访视的病灶数量与基线访视相同时计算总和
   - 计算相对基线的变化(CHG)和百分比变化(PCHG)
   - 标记PCHG最小的记录为最佳反应(BPCHGFL="Y")

## 数据截取处理

根据传入的cutoffdate参数，对ADTRT数据进行如下处理：

1. 先过滤掉ADT > cutoffdate的记录的靶病灶测量数据Diameter，后进行Sum of Diameter的运算

## 代码限制和注意事项

1. 函数依赖于特定的数据结构和变量命名规则，特别是TRT和TU数据集的结构
2. 函数需要ADSL数据集提供治疗开始日期(TRTSDT)信息
3. 函数使用simple_adam_gen辅助函数来生成基础数据集，这可能导致对该辅助函数的依赖
4. 病灶ID的提取基于TRREFID字段的特定格式，假设用逗号分隔并且第一部分是病灶ID
5. 基线记录(ABLFL)的标记基于ADY <= 1的条件和筛选访视的识别
6. 病灶直径总和(SUMDIAM)的计算要求当前访视的病灶数量与基线访视相同
7.  函数实现了通过病灶ID和访视名称在TRT和TU数据集之间的复杂匹配逻辑 