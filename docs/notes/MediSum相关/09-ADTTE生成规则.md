# ADTTE数据集生成规则文档

## 功能概述

`gen_adtte`函数的主要功能是根据原始EDC数据和规范(spec)生成ADTTE(Analysis Data Time to Event，分析用途的事件发生时间数据集)数据集。这个数据集包含临床试验中各受试者的生存分析数据，如总体生存期(OS)、无进展生存期(PFS)和缓解持续时间(DOR)等关键肿瘤疗效时间终点。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADTTE相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息
- `adresp`: ADRESP数据框，提供疗效评估信息和临床终点相关日期
- `adresp`: 用于判断“连续两次计划评估缺失”的参数（单位：周），可通过选项【连续缺失肿瘤评估判断窗口(>xx周则判断为连续缺失): (WEEKS)】组定义具体数值，默认数值为14。

## 输入和输出

- **输入**: 原始EDC数据、JSON规范、ADSL数据集和ADRESP数据集
- **输出**: 包含规范中要求的所有变量的ADTTE数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 从ADRESP中提取最佳总体疗效(BOR)相关记录：PARAMCD="BESTRESP"与PARAMCD="UBESTRESP"
2. 根据临床试验终点和删失(censoring)规则，为每个受试者标记不同的分组：
   - OS分组(os_group)
   - PFS分组(pfs_group)
   - DOR分组(dor_group)
3. 分别计算OS、PFS和DOR三个生存终点：
   - 计算事件或删失状态(CNSR)
   - 设置开始日期(STARTDT)和分析日期(ADT)
   - 标注事件描述(EVNTDESC)和删失日期描述(CNSDTDSC)
4. 计算各终点的时间值(AVAL、AVALD)
5. 合并所有终点数据，设置变量标签
6. 返回最终的ADTTE数据集

## ADRESP关键变量及其生成规则

ADTTE计算中使用了ADRESP数据集中的许多关键变量，这些变量的生成规则如下：

### 最佳总体疗效和评估标志

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| TUBASE | 是否有基线评估 | 基于TU：当`TUVISIT`为“SCREENING/筛选期”且`TUDAT`有效、且日期不晚于`cutoffdate`时，标记为"Y" |
| TUPOST | 是否有基线后评估 | 基于ADRS：存在`ADT`与`OVRLRESP`均非缺失的记录时标记为"Y" |
| AVALC | 最佳总体疗效(BOR) | 使用`bor_confirm_recist`函数计算，考虑确认窗口(默认CR/PR需28天确认，SD需42天持续) |
| F_CONFRM | 首次CR/PR确认日期 | 当BOR为CR/PR时，为所有满足确认规则的CR/PR记录中最早的ADT |

### 关键时间点变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| F_PD | 首次PD日期 | 从ADRS中筛选OVRLRESP="PD"的记录，取最早的ADT日期，是PFS事件的重要时间点 |
| F_CR | 首次CR日期 | 从ADRS中筛选OVRLRESP="CR"的记录，取最早的ADT日期 |
| F_PR | 首次PR日期 | 从ADRS中筛选OVRLRESP="PR"的记录，取最早的ADT日期 |
| F_PDDTH | 首次PD或死亡日期 | 计算F_PD和DTHDT中的最早日期 |
| L_AS | 最后一次充分评估日期 | 从ADRS中筛选OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期，是多种删失情况下的重要时间点 |
| F_ANTI | 首次抗肿瘤治疗日期 | 从CMFUCST.CMSTDAT、PRFURT.PRSTDAT、PRFUSURG.PRSTDAT中取最早日期(按年/月缺失补1后取最小)，用于新治疗删失 |
| L_AS_ANT | 抗肿瘤治疗前最后评估日期 | 从ADRS中筛选早于F_ANTI且OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期，用于新治疗删失 |
| L_BFPDDTH | PD/死亡前最后评估日期 | 从ADRS中筛选早于F_PDDTH且OVRLRESP不是"NE"且不为空的记录，取最晚的ADT日期，用于判断连续评估缺失 |
| F_CRPR | 首次CR/PR起始日期 | 确认DOR：F_CRPR = F_CONFRM；非确认UDOR：F_CRPR = min(F_PR, F_CR) |

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从ADSL.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从ADSL.SUBJID获取 |

### 参数变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| PARAM | 参数 | 根据终点类型设置值：<br>- "Overall Survival (Months)" <br>- "Progression Free Survival (Months)" <br>- "Duration of Response (Months)" <br>- "Unconfirmed Duration of Response (Months)" |
| PARAMCD | 参数代码 | 根据终点类型设置值：<br>- "OS" <br>- "PFS" <br>- "DOR" <br>- "UDOR" |

### 时间和事件变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STARTDT | 开始日期 | OS/PFS：使用随机或开始用药日期(RANDENDT)；DOR/UDOR：使用F_CRPR |
| ADT | 分析日期 | 具体赋值参考后续**分组与生存终点计算规则**部分 |
| AVAL | 时间(月) | 计算公式：(ADT - STARTDT + 1) / 30.4375 |
| AVALD | 时间(天) | 计算公式：ADT - STARTDT + 1 |
| CNSR | 删失状态 | 0 = 发生事件，1 = 删失 |

### 事件描述变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| EVNTDESC | 事件描述 | 具体赋值参考后续**分组与生存终点计算规则**部分 |
| EVNTDESN | 事件描述(数值) | 对应数值代码：OS为1/2/3；PFS与DOR/UDOR为3/4/5/6/7/8 |
| CNSDTDSC | 删失日期描述 | 具体赋值参考后续**分组与生存终点计算规则**部分 |

## 分组与生存终点计算规则

### OS分组(os_group)与计算规则

| os_group值 | 筛选条件 | 描述(中文) | CNSR | STARTDT | ADT | EVNTDESC | CNSDTDSC |
|------------|----------|------------|------|---------|-----|----------|----------|
| 1 | `is.na(DTHDT) & EOSSTT == "DISCONTINUED"` | 已终止研究，无死亡记录 | 1 | RANDENDT | LSTALVDT | "No Death, Discontinued from Study" | "Date Last Known Alive" |
| 2 | `is.na(DTHDT) & EOSSTT != "DISCONTINUED"` | 仍在研究中，无死亡记录 | 1 | RANDENDT | LSTALVDT | "No Death, Ongoing" | "Date Last Known Alive" |
| 3 | `!is.na(DTHDT)` | 死亡 | 0 | RANDENDT | DTHDT | "Death" | - |

**说明：**
- RANDENDT - 若受试者随机入组，则开始日期为随机日期；否则，开始日期为首次用药日期。
- LSTALVDT - 受试者末次生存日期。
- DTHDT - 死亡日期。

### PFS分组(pfs_group)与计算规则

| pfs_group值 | 筛选条件 | 描述(中文) | CNSR | STARTDT | ADT | EVNTDESC | CNSDTDSC |
|------------|----------|------------|------|---------|-----|----------|----------|
| 3 | `!is.na(F_ANTI) & (is.na(F_PDDTH) \| F_ANTI < F_PDDTH)` | 开始后续抗肿瘤治疗前未记录到PD或死亡 | 1 | RANDENDT | ifelse(is.na(L_AS_ANT), RANDENDT, L_AS_ANT) | "No Progressive Disease or Death before Anti-Cancer Therapy" | "Last assessment date before new anti-cancer therapy" |
| 4.1 | `is.na(TUPOST) & !is.na(DTHDT) & as.numeric(DTHDT) - as.numeric(RANDENDT) + 1 > miss_window*7` | 在连续缺失肿瘤评估后发生PD或死亡 | 1 | RANDENDT | RANDENDT | "Progressive Disease or Death after Consecutive Missed Tumor Assessments" | "Randomization date or Enrollment date" |
| 4.1 | `!is.na(F_PDDTH) & is.na(L_BFPDDTH) & as.numeric(F_PDDTH) - as.numeric(RANDENDT) +1 > miss_window*7` | 在连续缺失肿瘤评估后发生PD或死亡 | 1 | RANDENDT | RANDENDT | "Progressive Disease or Death after Consecutive Missed Tumor Assessments" | "Randomization date or Enrollment date" |
| 4.2 | `!is.na(F_PDDTH) & !is.na(L_BFPDDTH) & as.numeric(F_PDDTH) - as.numeric(L_BFPDDTH) +1 > miss_window*7` | 在连续缺失肿瘤评估后发生PD或死亡 | 1 | RANDENDT | L_BFPDDTH | "Progressive Disease or Death after Consecutive Missed Tumor Assessments" | "Last assessment date before two missed consecutive planned tumor assessments" |
| 5 | `is.na(F_PDDTH) & EOSSTT == "DISCONTINUED"` | 已终止研究，无PD或死亡记录 | 1 | RANDENDT | ifelse(is.na(L_AS), RANDENDT, L_AS) | "No Progressive Disease or Death, Discontinued from Study" | "Last assessment date" |
| 6 | `is.na(F_PDDTH) & EOSSTT != "DISCONTINUED"` | 仍在研究中，无PD或死亡记录 | 1 | RANDENDT | ifelse(is.na(L_AS), RANDENDT, L_AS) | "No Progressive Disease or Death, Ongoing in Study" | "Last assessment date" |
| 7 | `!is.na(F_PD)` | 疾病进展 | 0 | RANDENDT | F_PD | "Progressive Disease" | "First progression disease date" |
| 8 | `!is.na(DTHDT)` | 死亡 | 0 | RANDENDT | DTHDT | "Death without Progression" | "Death date" |

**说明：**
- RANDENDT - 若受试者随机入组，则开始日期为随机日期；否则，开始日期为首次用药日期。
- L_AS_ANT - 抗肿瘤治疗前最后评估日期。
- L_BFPDDTH - PD/死亡前最后评估日期。
- L_AS - 最后一次评估日期。
- F_PD - 首次PD日期。
- DTHDT - 死亡日期。
- `miss_window`为周数参数(默认14)，可通过选项【连续缺失肿瘤评估判断窗口(>xx周则判断为连续缺失): (WEEKS)】组定义具体数值，用于判断“连续两次计划评估缺失”的时间阈值。

### DOR/UDOR分组(dor_group)与计算规则

| dor_group值 | 筛选条件 | 描述(中文) | CNSR | STARTDT | ADT | EVNTDESC | CNSDTDSC |
|------------|----------|------------|------|---------|-----|----------|----------|
| 3 | `AVALC %in% c("CR", "PR") & !is.na(F_ANTI) & (is.na(F_PDDTH) \| F_ANTI < F_PDDTH)` | 开始后续抗肿瘤治疗前未记录到PD或死亡 | 1 | F_CRPR | ifelse(is.na(L_AS_ANT), F_CRPR, L_AS_ANT) | "No Progressive Disease or Death before New Anti-Cancer Therapy" | "Last assessment date before new anti-cancer therapy" |
| 4.2 | `AVALC %in% c("CR", "PR") & !is.na(F_PDDTH) & !is.na(L_BFPDDTH) & as.numeric(F_PDDTH) - as.numeric(L_BFPDDTH) +1 > miss_window*7` | 在连续缺失肿瘤评估后发生PD或死亡 | 1 | F_CRPR | L_BFPDDTH | "Progressive Disease or Death after Consecutive Missed Tumor Assessments" | "Last assessment date before two missed consecutive planned tumor assessments" |
| 5 | `AVALC %in% c("CR", "PR") & is.na(F_PDDTH) & EOSSTT == "DISCONTINUED"` | 已终止研究，无PD或死亡记录 | 1 | F_CRPR | ifelse(is.na(L_AS), F_CRPR, L_AS) | "No Progressive Disease or Death, Discontinued from Study" | "Last assessment date" |
| 6 | `AVALC %in% c("CR", "PR") & is.na(F_PDDTH) & EOSSTT != "DISCONTINUED"` | 仍在研究中，无PD或死亡记录 | 1 | F_CRPR | ifelse(is.na(L_AS), F_CRPR, L_AS) | "No Progressive Disease or Death, Ongoing in Study" | "Last assessment date" |
| 7 | `AVALC %in% c("CR", "PR") & !is.na(F_PD)` | 疾病进展 | 0 | F_CRPR | F_PD | "Progressive Disease" | "First progression disease date" |
| 8 | `AVALC %in% c("CR", "PR") & !is.na(DTHDT)` | 死亡 | 0 | F_CRPR | DTHDT | "Death without Progression" | "Death date" |

**说明：**
- F_CRPR - 对于确认DOR计算时，使用F_CONFRM；对于非确认UDOR计算时，使用min(F_PR, F_CR)。
- L_AS_ANT - 抗肿瘤治疗前最后评估日期。
- L_BFPDDTH - PD/死亡前最后评估日期。
- L_AS - 最后一次评估日期。
- F_PD - 首次PD日期。
- DTHDT - 死亡日期。
- `miss_window`为周数参数(默认14)，可通过选项【连续缺失肿瘤评估判断窗口(>xx周则判断为连续缺失): (WEEKS)】组定义具体数值，用于判断“连续两次计划评估缺失”的时间阈值。

## 代码限制和注意事项

1. 函数依赖于ADRESP数据集中的关键日期变量，包括F_PD、F_CR、F_PR、L_AS、L_AS_ANT、F_ANTI、F_PDDTH和L_BFPDDTH等。
2. 生存时间的月份计算使用了30.4375作为每月的平均天数。
3. PFS和DOR终点的删失规则涉及多种临床情况，包括连续评估缺失、新治疗和研究终止等；连续缺失的时间阈值由`miss_window`(默认14周)控制。
4. 对于DOR分析：确认DOR以`F_CONFRM`作为起始(F_CRPR)，非确认UDOR以`min(F_PR, F_CR)`作为起始(F_CRPR)。
5. 事件描述(EVNTDESC)在实现中固定为上述英文短语，应与TFL或标准输出保持一致。 