# 08-ADRESP数据集生成规则文档

## 功能概述

`gen_adresp`函数的主要功能是根据原始EDC数据和规范(spec)生成ADRESP(Analysis Data Response，分析用途的肿瘤疗效评估总结数据集)数据集。这个数据集对ADRS(疗效评估数据)和ADTRT(靶病灶数据)中的信息进行整合和汇总，计算最佳总体疗效(BOR)、客观缓解率(ORR)、疾病控制率(DCR)等关键肿瘤疗效评估指标。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADRESP相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息
- `cutoffdate`: 主要的数据截止日期，默认为当前系统日期
- `subjid`: 受试者ID变量名，默认为"SUBJID"
- `crpr_window`: CR/PR确认窗口，默认为28天
- `sd_window`: SD确认窗口，默认为42天
- `adrs`: ADRS数据框，提供肿瘤疗效评估信息
- `adtr`: ADTRT数据框，提供靶病灶评估信息

## 输入和输出

- **输入**: 原始EDC数据、JSON规范、ADSL数据集、ADRS数据集和ADTRT数据集
- **输出**: 包含规范中要求的所有变量的ADRESP数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 提取规范中定义的依赖关系信息
2. 计算最佳总体疗效(BOR)，包括考虑确认窗口的确认反应
3. 标记受试者是否有基线评估(TUBASE)和基线后评估(TUPOST)
4. 基于BOR计算客观缓解率(ORR)和疾病控制率(DCR)
5. 计算无确认要求的非确认最佳总体疗效(uBOR)及相应的反应率
6. 从ADRS中提取各种关键日期信息(首次PD、CR、PR、SD日期等)
7. 处理抗肿瘤治疗信息，确定首次抗肿瘤治疗日期
8. 合并ADSL中的重要日期信息
9. 添加额外的日期计算字段
10. 设置变量标签
11. 返回最终的ADRESP数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从ADSL.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从ADSL.SUBJID获取 |
| TUBASE | 是否有基线评估 | 根据TU中TUVISIT为"SCREENING"/"筛选期"且TUDAT有效、且日期不晚于`cutoffdate`的最早记录，标记为"Y" |
| TUPOST | 是否有基线后评估 | 根据ADRS中有效的评估记录(ADT和OVRLRESP不为空)标记为"Y" |

### 疗效参数变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PARAM | 参数 | 根据评估类型设置值：<br>- "Best Overall Response"<br>- "Unconfirmed Best Overall Response"<br>- "Objective Response"<br>- "Unconfirmed Objective Response"<br>- "Disease Control"<br>- "Unconfirmed Disease Control" |
| PARAMCD | 参数代码 | 根据PARAM设置相应代码：<br>- "BESTRESP"<br>- "UBESTRESP"<br>- "OBJRESP"<br>- "UOBJRESP"<br>- "DISCTRL"<br>- "UDISCTRL" |

### 疗效评估变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AVALC | 分析值(字符型) | 根据PARAMCD不同设置不同值：<br>- 对于BOR/uBOR：记录最佳总体疗效评价结果<br>- 对于ORR/uORR：若BOR/uBOR为CR或PR，则为"Responder"，否则为"Non Responder"<br>- 对于DCR/uDCR：若BOR/uBOR为CR、PR或SD，则为"Responder"，否则为"Non Responder" |
| AVAL | 分析值 | 对于ORR和DCR相关参数：<br>- 若AVALC为"Responder"，则为1<br>- 若AVALC为"Non Responder"，则为0 |

### 时间点变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| F_PD | 首次PD日期 | 从ADRS中筛选OVRLRESP="PD"的记录，取最早的ADT日期 |
| F_CR | 首次CR日期 | 从ADRS中筛选OVRLRESP="CR"的记录，取最早的ADT日期 |
| F_PR | 首次PR日期 | 从ADRS中筛选OVRLRESP="PR"的记录，取最早的ADT日期 |
| F_CONFRM | 首次CR/PR确认日期 | 当BOR为CR或PR时，取所有被判定为CR/PR且满足确认规则的记录中的最早ADT |
| F_SD | 首次SD日期 | 从ADRS中筛选OVRLRESP="SD"的记录，取最早的ADT日期 |
| L_AS | 最后一次充分评估日期 | 从ADRS中筛选OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期 |
| F_ANTI | 首次抗肿瘤治疗日期 | 从CMFUCST.CMSTDAT、PRFURT.PRSTDAT和PRFUSURG.PRSTDAT中选取最早的日期(按年/月/日缺失补齐至1进行推断，再取最小) |
| L_AS_ANT | 抗肿瘤治疗前最后一次充分评估日期 | 从ADRS中筛选早于F_ANTI且OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期 |

### ADSL相关变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| RANDENDT | 随机或开始给药日期 | 优先使用ADSL.RANDDT，如果为空则使用ADSL.TRTSDT |
| TRTSDT | 治疗开始日期 | 从ADSL.TRTSDT获取 |
| TRTEDT | 治疗结束日期 | 从ADSL.TRTEDT获取 |
| DTHDT | 死亡日期 | 从ADSL.DTHDT获取 |
| LSTALVDT | 最后已知存活日期 | 从ADSL.LSTALVDT获取 |
| EOSSTT | 研究结束状态 | 从ADSL.EOSSTT获取 |

### 计算的日期变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| F_PDDTH | 首次PD或死亡日期 | 计算F_PD和DTHDT中的最早日期(两者皆缺失则为空) |
| L_BFPDDTH | 首次PD或死亡前最后一次充分评估日期 | 从ADRS中筛选早于F_PDDTH且OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期 |
| RSPDURM | 达到反应的时间(月) | 对UBESTRESP且uPR/uCR：(min(F_PR,F_CR) - RANDENDT + 1)/30.4375；对BESTRESP且PR/CR：(F_CONFRM - RANDENDT + 1)/30.4375；其余为空 |

## 最佳总体疗效(BOR) 评估规则

### 最佳总体疗效(BOR)数据处理步骤

在使用`bor_confirm_recist`函数计算确认的BOR之前，对ADRS数据进行了以下整理：

1. 仅保留`ADY`非缺失的记录，并按`SUBJID`、`ADT`排序后编号。
2. 移除首次`OVRLRESP = "PD"`之后的所有评估。
3. 根据“确认的最佳总体疗效(BOR)计算规则”对每个评估结果进行判断，并取受试者能确认的最佳结果（CR > PR > `NON-CR/NON-PD`/SD > PD > NE），作为最佳总体疗效(BOR)。

### 确认的最佳总体疗效(BOR)计算规则

| 第一次评估 | 第二次评估 | 第三次评估 | 判断条件 | 结果 |
|---|---|---|---|---|
| **CR** | CR | - | x2_ady - x1_ady + 1 ≥ crpr_window | CR |
|  | CR | - | 不满足上条，x1_ady ≥ sd_window | SD |
|  | CR | - | 不满足上条，x1_ady < sd_window | NE |
|  | PR/SD/PD | - | x1_ady ≥ sd_window | SD |
|  | PR/SD/PD | - | x1_ady < sd_window | PD |
|  | NE | CR | 后续存在CR且与首次CR最大间隔≥crpr_window | CR |
|  | NE | 任意 | 不满足上条，x1_ady ≥ sd_window | SD |
|  | NE | 任意 | 不满足上条，x1_ady < sd_window | NE |
|  | 无后续评估 | - | x1_ady ≥ sd_window | SD |
|  | 无后续评估 | - | x1_ady < sd_window | NE |
| **PR** | PR | - | 存在任意满足最大间隔≥crpr_window的PR-PR序列 | PR |
|  | CR/PR | - | x2_ady - x1_ady + 1 ≥ crpr_window | PR |
|  | CR/PR | - | 不满足上条，x2_ady ≥ sd_window  | SD |
|  | CR/PR | - | 不满足上条，x2_ady < sd_window | NE |
|  | SD | PR/CR | 与PR/CR间最大间隔≥crpr_window | PR |
|  | SD | 任意 | 不满足上条 | SD |
|  | PD | - | x1_ady ≥ sd_window | SD |
|  | PD | - | x1_ady < sd_window | PD |
|  | NE | PR/CR | 与首次PR的最大间隔≥crpr_window | PR |
|  | NE | - | 不满足上条，x1_ady ≥ sd_window  | SD |
|  | NE | - | 不满足上条，x1_ady < sd_window | NE |
| **SD** | PD | - | x1_ady ≥ sd_window | SD |
|  | PD | - | x1_ady < sd_window | PD |
|  | CR/PR/SD/NE/`NON-CR/NON-PD` | - | x1_ady ≥ sd_window | SD |
|  | CR/PR/SD/NE/`NON-CR/NON-PD` | - | x1_ady < sd_window  | NE |
| **`NON-CR/NON-PD`** | PD | - | x1_ady ≥ sd_window | SD |
|  | PD | - | x1_ady < sd_window | PD |
|  | CR/PR/SD/NE/`NON-CR/NON-PD` | - | x1_ady ≥ sd_window | `NON-CR/NON-PD` |
|  | CR/PR/SD/NE/`NON-CR/NON-PD` | - | x1_ady < sd_window | NE |
| **PD** | - | - | 直接判断为 PD | PD |
| **NE** | - | - | 直接判断为 NE | NE |

## 非确认的最佳总体疗效(uBOR)评估规则

对于无需确认的uBOR计算，使用了不同的逻辑：

1. 对于SD评估，仍要求满足最小持续时间(sd_window)，即ADY ≥ sd_window。
2. 首先确定首次PD日期(F_PD_p)，只考虑该日期及之前的评估。
3. 根据OVRLRESP的数值优先级选择最佳反应：CR > PR > `NON-CR/NON-PD` > SD > PD > NE。
4. 将最佳反应标记为uCR、uPR等，以区分于确认的反应。

### 案例展示 - uBOR
假设 sd_window=42，以下是一些特殊案例的uBOR分析结果：

| 案例 | 评估序列 | BOR判断 | 说明 |
|------|----------|---------|------|
| 特殊案例1 | SD (D43) | SD | 首次为疗评且疗评日期≥sd_window，即判定为SD |
| 特殊案例2 | SD (D41) | NE | 首次为疗评且疗评日期<sd_window，且无后续疗评，即判定为NE |

## 客观缓解率(ORR)和疾病控制率(DCR)计算规则

1. 客观缓解率(ORR)：
   - 若BOR为CR或PR，则记为"Responder"(AVAL=1)
   - 否则记为"Non Responder"(AVAL=0)

2. 非确认客观缓解率(uORR)：
   - 若uBOR为uCR或uPR，则记为"Responder"(AVAL=1)
   - 否则记为"Non Responder"(AVAL=0)

3. 疾病控制率(DCR)：
   - 若BOR为CR、PR或SD，则记为"Responder"(AVAL=1)
   - 否则记为"Non Responder"(AVAL=0)

4. 非确认疾病控制率(uDCR)：
   - 若uBOR为uCR、uPR或SD，则记为"Responder"(AVAL=1)
   - 否则记为"Non Responder"(AVAL=0)

## 代码限制和注意事项

1. 函数依赖于特定格式的ADRS和ADTRT数据集，这两个数据集应该已经按照CDISC标准规范生成。
2. 函数需要`bor_confirm_recist`辅助函数来计算确认的最佳总体疗效。
3. CR/PR和SD的确认窗口可通过参数`crpr_window`和`sd_window`调整，默认分别为28天和42天。
4. 函数假设`OVRLRESP`变量已经标准化，能够识别"CR"、"PR"、"SD"、"NON-CR/NON-PD"、"PD"和"NE"等值。
5. 关于PD：BOR与uBOR均仅在逻辑上移除首次PD之后的评估记录进行判断。
6. 关于抗肿瘤治疗：函数提供`F_ANTI`与`L_AS_ANT`用于分析，但当前BOR计算未强制排除抗肿瘤治疗后的评估；是否排除由后续分析或TFL层面决定。
7.  抗肿瘤治疗日期在存在年或月缺失时按1进行日期补全后取最小值。 
8.  该数据集生成是基于数据截取之后的ADSL，ADRS和ADTRT数据集，故无需进行额外的数据截取处理。