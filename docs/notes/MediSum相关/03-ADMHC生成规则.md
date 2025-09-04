# ADMHC数据集生成规则文档 

## 功能概述

`gen_admhc`函数的主要功能是根据原始EDC数据和规范(spec)生成ADMH_C(Analysis Data Medical History for Cancer，分析用途的肿瘤病史数据集)数据集。这个数据集包含临床试验中各受试者的肿瘤相关病史信息，如初始诊断日期、疾病部位、TNM分期、复发/转移情况等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADMH_C相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息

## 输入和输出

- **输入**: 原始EDC数据、JSON规范和ADSL数据集
- **输出**: 包含规范中要求的所有变量的ADMH_C数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 从名称以MHC开头的数据集中提取所需变量
3. 根据ADSL提供的日期信息，计算疾病持续时间并进行日期缺失值填补
4. 对所有MHC开头的数据集进行处理并合并
5. 设置变量标签
6. 返回最终的ADMHC数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从MHC.STUDYCODE或MHC.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从MHC.SUBJID获取 |

### 疾病信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| MHCAT | 病史分类 | 从MHC.TNAME获取 |
| MHLOC | 解剖学位置 | 从MHC.MHLOC获取 |

### 诊断日期和疾病持续时间变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| DIAGDTC | 初始病理诊断日期 | 从MHC.MHDAT或MHC.MHIDAT获取 |
| DIAGDT | 初始病理诊断日期(数值) | 对DIAGDTC进行缺失值填补：<br>1. 完全缺失年份则不进行填补<br>2. 缺失月份则使用1月<br>3. 缺失日期则使用1日 |
| DISCOUR | 疾病过程(月) | 计算公式：(TRTSDT-DIAGDT+1)/30.4375，结果四舍五入到小数点后2位 |
| PDDTC | 最近进展/复发日期 | 从MHC.MHLPDDAT获取 |
| PDDT | 最近进展/复发日期(数值) | 对PDDTC进行缺失值填补：<br>1. 完全缺失年份则不进行填补<br>2. 缺失月份则使用1月<br>3. 缺失日期则使用1日 |
| PDCOUR | 疾病进展过程(月) | 计算公式：(参考日期-PDDT+1)/30.4375，其中参考日期优先使用RANDDT，其次是ENRLDT，最后是TRTSDT，结果四舍五入到小数点后2位 |

### 分期和病理信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| MHHG | 初始诊断时的组织学分级 | 从MHC.MHHG获取 |
| MHTNMT | 初始TNM分期(T) | 从MHC.MHTNMT获取 |
| MHTNMN | 初始TNM分期(N) | 从MHC.MHTNMN获取 |
| MHTNMM | 初始TNM分期(M) | 从MHC.MHTNMM获取 |
| MHCT | 初始诊断时的临床分期 | 从MHC.MHCT获取 |
| MHLHG | 筛选时的组织学分级 | 从MHC.MHLHG获取 |
| MHLTNMT | 当前TNM分期(T) | 从MHC.MHLTNMT获取 |
| MHLTNMN | 当前TNM分期(N) | 从MHC.MHLTNMN获取 |
| MHLTNMM | 当前TNM分期(M) | 从MHC.MHLTNMM获取 |
| MHLCT | 筛选时的临床分期 | 从MHC.MHLCT获取 |
| MHHCS | 病理类型 | 从MHC.MHHCS获取 |
| MHRM | 任何复发/转移 | 从MHC.MHRM获取 |
| MHMLOC | 转移部位 | 从MHC.MHMLOC获取 |
| MHMLOCO | 转移部位其他，请说明 | 从MHC.MHMLOCO获取 |

## 日期计算和填补规则

该函数对日期变量有特定的处理规则：

1. **DIAGDT(初始诊断日期)的处理**：
   - 如果DIAGDTC缺失年份，则DIAGDT为空值(NA)
   - 如果DIAGDTC缺失月份，则月份填补为1月
   - 如果DIAGDTC缺失日期，则日期填补为1日

2. **PDDT(最近进展日期)的处理**：
   - 如果PDDTC缺失年份，则PDDT为空值(NA)
   - 如果PDDTC缺失月份，则月份填补为1月
   - 如果PDDTC缺失日期，则日期填补为1日

3. **疾病持续时间计算**：
   - DISCOUR = (TRTSDT-DIAGDT+1)/30.4375
   - PDCOUR = (参考日期-PDDT+1)/30.4375，其中参考日期优先使用RANDDT，其次是ENRLDT，最后是TRTSDT

## 代码限制和注意事项

1. 该函数依赖于特定的数据结构和变量命名规则
2. 函数需要ADSL数据集提供关键的日期信息（如RANDDT、ENRLDT、TRTSDT）
3. DISCOUR和PDCOUR的计算都基于30.4375天/月的转换因子
4. 函数会处理所有以MHC开头的数据集，并将结果合并
5. 日期缺失值的填补规则仅适用于部分缺失的日期（如只缺月份或日期），完全缺失的日期不进行填补
6. 该函数不考虑数据截止日期(cutoffdate)的数据截取处理
7. 疾病持续时间(DISCOUR)和疾病进展过程(PDCOUR)均为计算值，取决于相关日期的准确性 