# 07-ADRS数据集生成规则文档

## 功能概述

`gen_adrs`函数的主要功能是根据原始EDC数据和规范(spec)生成ADRS(Analysis Data Response，分析用途的肿瘤疗效评估数据集)数据集。这个数据集包含临床试验中各受试者的肿瘤疗效评估信息，如总体疗效、靶病灶响应、非靶病灶响应和新病灶指示等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADRS相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息
- `cutoffdate`: 主要的数据截止日期

## 输入和输出

- **输入**: 原始EDC数据、JSON规范和ADSL数据集
- **输出**: 包含规范中要求的所有变量的ADRS数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 使用simple_adam_gen函数从原始数据中生成基础数据集
3. 从肿瘤评估数据(TU)中提取分析日期(ADT)信息，对每次访视计算最早和最晚日期
4. 标准化总体疗效响应(OVRLRESP)的值，将不同语言和表达方式的响应统一为标准代码
5. 根据总体响应类型设置分析日期：进展性疾病(PD)使用最早日期，其他使用最晚日期
6. 添加ADSL中的治疗开始日期，计算相对日期(ADY)
7. 根据截止日期处理数据
8. 设置变量标签
9. 返回最终的ADRS数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从RS.STUDYCODE或RS.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从RS.SUBJID获取<br>匹配TU变量：TU.SUBJID |

### 分类和状态变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PARCAT1 | 参数类别 | 固定值："Recist 1.1" |
| RSSTAT | 是否进行了评估 | 如果RS.RSYN为"否"、"No"、"N"或"NO"，则为"NOT DONE"，否则为空值(NA) |
| RSREASND | 未完成原因 | 从RS.RSREAS获取 |

### 疗效评估变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| TRGRESP | 靶病灶响应 | 从RS.TRGRESP获取 |
| NTRGRESP | 非靶病灶响应 | 从RS.NTRGRESP获取 |
| NEWLIND | 新病灶指示 | 从RS.NEWLIND获取 |
| OVRLRESP | 总体响应 | 从RS.OVRLRESP获取，并进行标准化：<br>- "CR", "完全缓解(CR)", "Complete Remission (CR)" → "CR"<br>- "PR", "部分缓解(PR)", "Partial Remission (PR)" → "PR"<br>- "SD", "疾病稳定(SD)", "Stable Disease (SD)" → "SD"<br>- "NON-CR/NON-PD", "Non-CR/Non-PD", "非完全缓解/非疾病进展(非CR/非PD)" → "Non-CR/Non-PD"<br>- "PD", "疾病进展(PD)", "Progressive Disease (PD)" → "PD"<br>- "NE", "无法评估(NE)", "Not Evaluable (NE)" → "NE"<br>- "NED", "无病灶(NED)" → "NED" |

### 访视和日期变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AVISIT | 分析访视 | 从RS.RSVISIT获取<br>匹配TU变量：TU.TUVISIT |
| ADT | 分析日期 | 根据总体响应(OVRLRESP)类型设置：<br>- 如果OVRLRESP="PD"，使用该访视中TU.TUDAT的最早日期<br>- 如果OVRLRESP不是"PD"，使用该访视中TU.TUDAT的最晚日期 |
| ADY | 分析相对日 | 计算公式：<br>- 如果ADT >= TRTSDT，则ADY = ADT - TRTSDT + 1<br>- 如果ADT < TRTSDT，则ADY = ADT - TRTSDT |

## 数据截取处理

根据传入的cutoffdate参数，对ADRS数据进行如下处理：

1. 过滤掉ADT > cutoffdate的记录

## 代码限制和注意事项

1. 函数依赖于特定的数据结构和变量命名规则
2. 函数需要ADSL数据集提供治疗开始日期(TRTSDT)信息
3. 函数使用simple_adam_gen辅助函数来生成基础数据集，这可能导致对该辅助函数的依赖
4. ADT的确定策略特别针对肿瘤疗效评估的临床意义：PD使用最早日期（表示最早观察到进展），非PD使用最晚日期（表示最长观察到的稳定/缓解状态）
5. 函数对OVRLRESP变量进行了标准化处理，能够处理多种语言（英文和中文）和不同表达方式的响应值
6. ADRS数据集是肿瘤临床试验中的关键疗效评估数据集，通常用于生存分析和疗效评估
7. 该函数处理了RS和TU两个数据源的信息，需要在同一访视下匹配它们的数据 