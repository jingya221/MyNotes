# 01-ADSL数据集生成规则文档

## 功能概述

`gen_adsl`函数的主要功能是根据原始EDC数据和规范(spec)生成ADSL(Analysis Data Subject Level，分析用途的受试者水平数据集)数据集。这个数据集包含临床试验中每个受试者的关键信息，如人口统计学特征、入组和随机化信息、治疗情况、试验状态等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADSL相关的JSON规范列表
- `cutoffdate`: 主要的数据截止日期，用于派生和截断记录
- `cycleday`: 主要传递值，用于派生EESFL（有效性评估人群标志）
- `subjid`: 默认为"SUBJID"，如果标准EDC变更则会改变
- `openlabel`: 主要传递值，如果为F则不会派生TRT01P和TRT01A

## 输入和输出

- **输入**: 原始EDC数据和JSON规范
- **输出**: 包含规范中要求的所有变量的数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. 从EDC原始数据中提取相关数据
2. 处理数据：直接派生、基于依赖关系派生、提取基线值、派生多重依赖变量等
3. 根据截止日期处理数据
4. 设置变量标签
5. 返回最终的ADSL数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 直接从SUBJECT.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 直接从SUBJECT.SUBJID获取 |
| SITEID | 研究中心标识符 | 直接从SUBJECT.SITEID获取 |

### 筛选和入组变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| SCRNFFL | 筛选失败标志 | 如果DSENROLL.DSCAT为"Screen Failure"或"筛选失败"，则为"Y"，否则为空值(NA) |
| SCRNFRS | 筛选失败原因 | 如果SCRNFFL为"Y"，则为DSENROLL.DSDECOD |
| ENRLFL | 入组人群标志 | 如果DSENROLL.DSCAT为"Screen Success"或"筛选成功"，则为"Y"，否则为空值(NA) |
| ENRLDT | 入组日期 | 从DSENROLL.DSSTDAT获取；若未收集且无RANDDT，则使用TRTSDT/RFICDT |

### 随机化变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| RANDDT | 随机化日期 | 从DSRAND.RANDDATE获取 |
| RANDFL | 随机化人群标志 | 如果DSRAND.RANDFL为"是"或"Yes"，则为"Y"，否则为空值(NA) |

### 治疗相关变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| TRTSDT | 首次接触治疗日期 | 从所有以EX开头的数据集中获取，筛选EXSTDAT/EXENDAT，要求EXDSTXT>0或为"UK"；取最小日期并应用cutoff |
| TRTEDT | 最后接触治疗日期 | 从所有以EX开头的数据集中获取，筛选EXSTDAT/EXENDAT，要求EXDSTXT>0或为"UK"；取最大日期并应用cutoff |
| TRT01P | 计划的第01期治疗 | 开放标签试验：优先从DSENROLL中按字段前缀`DOSELVL`/`REGIMEN`收集所有可用项（以“变量标签:值”的形式），多项以", "拼接；若DSENROLL缺失且存在DSRAND页面，则使用DSRAND中`REGIMEN`/`DOSELVL`收集并拼接；若仍缺失且ENRLFL非缺失，则设为"N/A"。 |
| TRT01A | 实际的第01期治疗 | 若TRTSDT非缺失，则=TRT01P；否则为空值(NA) |
| EOTSTTx | 结束治疗状态x | 如果DSEOTx.DSDECOD不为空，则为"DISCONTINUED"；若TRTSDT不为空且DSEOTx.DSDECOD为空，则为"ONGOING" |
| EOTDTx | 结束治疗日期x | 从DSEOTx.DSSTDAT获取（数值化），应用cutoff |
| DCTREASx | 停止治疗原因x | 从DSEOTx.DSDECOD获取 |
| DCTRESPx | 停止治疗具体原因x | 从DSEOTx.DSTERM获取 |

### 研究状态变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| EOSSTT | 研究结束状态 | 若DSEOS.DSDECOD不为空则为"DISCONTINUED"；否则若RANDDT不为空或TRTSDT不为空，则为"ONGOING" |
| EOSDT | 研究结束日期 | 从DSEOS.DSSTDAT获取（日期数值化），应用cutoff |
| DCSREAS | 研究中止原因 | 从DSEOS.DSDECOD获取，若EOSDT超过cutoff且无DTHDT则设为缺失 |
| DCSRESP | 研究中止具体原因 | 从DSEOS.DSTERM获取，若EOSDT超过cutoff且无DTHDT则设为缺失 |

### 人口学变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| BRTHDT | 出生日期 | 从DM.BRTHDAT获取 |
| RFICDT | 知情同意日期 | 从SUBJECT.RFICDAT或DM.RFICDAT获取 |
| AGE | 年龄 | 计算公式：floor((RFICDT-BRTHDT+1)/365.25) |
| AGEU | 年龄单位 | 固定为"Years" |
| AGEGR1 | 年龄组1 | 如果AGE<65，则为"<65"；如果AGE>=65，则为">=65" |
| SEX | 性别 | 从DM.SEX获取 |
| RACE | 种族 | 从DM.RACE获取 |
| ETHNIC | 民族 | 从DM.ETHNIC获取 |
| CETHNIC | 收集的民族 | 如果DM.CETHNIC为"Other"或"其他"，则为DM.CETHNICO，否则为DM.CETHNIC |
| PSUBJID | 先前的受试者ID | 从DM.PSUBJID获取 |

### 基线评估变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| BLHTCM | 基线身高(cm) | 从DM.HEIGHT获取 |
| BLWTKG | 基线体重(kg) | 获取第一个非缺失的VSWT.WEIGHT（按VSDAT排序取最早） |
| BLBMI | 基线体重指数(kg/m^2) | 计算公式：round(BLWTKG/(BLHTCM/100)^2, 2) |
| BLECOG | 基线ECOG评分 | 获取第一个非缺失的QSECOG.QSORRES / RSECOG.RSORRES （按QSDAT或RSDAT日期排序取最早）|
| ALCOST | 饮酒使用情况 | 从SUALCO.SUNCF获取 |
| CIGRST | 烟草使用情况 | 从SUCIGR.SUNCF获取 |

### 分层因素

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| RSFx | 分层因素x | 从DSRSF.DSRSFx或DSENROLL.DSRSFx获取；保留多项 |

### 人群标志变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| ITTFL | 意向治疗人群标志 | 如果RANDFL/ENRLFL为"Y"，则为"Y"，否则为"N" |
| FASFL | 全分析集人群标志 | 如果TRTSDT不为空，则为"Y"，否则为"N" |
| SAFFL | 安全性人群标志 | 如果TRTSDT不为空，则为"Y"，否则为"N" |
| EESFL | 有效性评估人群标志 | 1. 默认定义: 所有入组并至少使用一次试验药物的受试者，尚在研究中且尚未达到首次基线后肿瘤评估时间的受试者除外。当FASFL="Y"且受试者未退出治疗且截止日期 < 起始日期(startdt)+2×`cycleday`时标记为"N"且TU中不存在基线后非筛选期且不晚于截止日期的影像学检查记录时，标记为"N"，其余情况为"Y"。<br>2. 基于具有基线可测量靶病灶的受试者+默认定义。在按照默认定义判断后，仅保留`ADTRT`中`PARAMCD="DIAMETER"`且`ABLFL="Y"`的受试者EESFL不变，其余赋值为"N"。<br>3. 基于具有基线病灶的受试者+默认定义。在按照默认定义判断后，仅保留`ADRESP`中`TUBASE="Y"`的受试者EESFL不变，其余赋值为"N"。<br>**注意：<br>`startdt`取TRTSDT/ENRLDT/RANDDT三者中的最早非缺失值。<br>`cycleday`来源于自定义选项【1. 项目一周期天数设为xx天】。<br>`ADRESP`中`TUBASE`规则：根据TU中TUVISIT为"SCREENING"/"筛选期"且TUDAT有效、且日期不晚于`cutoffdate`的最早记录，标记为"Y"。**|

### 死亡和随访变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| DTHFL | 受试者死亡标志 | 如果DSEOS.DSDECOD为"Death"或"死亡"，或DTHDTC非空，则为"Y"；当死亡日期>截取日期时会设为空 |
| DTHDTC | 死亡日期 | 优先使用DSEOS.DTHDAT；若缺失且DSEOS.DSDECOD为"Death"/"死亡"，则使用DSEOS.DSSTDAT；保留字符型原样（支持部分日期，例如含"UK"） |
| DTHDT | 死亡日期(数值) | 见下面“DTHDT生成逻辑”；若推算出的DTHDT>cutoffdate，则设为NA并同时将DTHFL设为空 |
| DTHCAUS | 死亡原因 | 从DSEOS.DTHREAS获取 |
| LSTALVDT | 最后已知存活日期 | 见下面“LSTALVDT生成逻辑” |

## 数据截取处理

该函数根据传入的cutoffdate参数对多个日期变量进行截止处理：

1. RFICDT: 过滤掉RFICDT > cutoffdate的记录
2. EX数据: 过滤掉EXSTDAT > cutoffdate的记录，并将EXENDAT > cutoffdate的值设为cutoffdate
3. EOT数据: 过滤掉EOTDT > cutoffdate的记录
4. LSTALVDT: 如果LSTALVDT > cutoffdate，则设为cutoffdate
5. DTHDT: 如果DTHDT > cutoffdate，则设为空值(NA)，并将DTHFL设为空值(NA)
6. EOSDT: 如果EOSDT > cutoffdate，则设为空值(NA)，并将EOSSTT、DCSREAS、DCSRESP设为空值(NA)

## LSTALVDT和DTHDT变量生成逻辑及cutoffdate处理详细描述

### LSTALVDT (最后已知存活日期)生成逻辑：

1. 从JSON规范comment字段中指定的数据集获取日期信息，这些数据集包括：VS, VSWT, PE, QS, LB, EG, CVLVEF, PC, MI, PRSURG, AE, CM , PRCND, PRCRT, PRCCRT, PRCSURG, EX, CMFUCST, PRFURT, PTFUSURG, PRFULT, TU, SS_NLF, DSEOS_NLF 
2. 排除SS.SSORRES/DSEOS.DSDECOD为"Lost to Follow-up"或"失访"的记录（通过toupper函数处理大小写）
3. 排除SS.SSORRES为"Death", "死亡"的记录；当DSEOS.DSDECOD为"Death", "死亡"时，置空其DSSTDAT（不作为LSTALVDT来源）
4. 处理不完整日期：
   - 对于包含"UK"的日期（表示日期的某部分未知），使用"01"替换"UK"进行推算
   - 如果日期中包含超过2个"UK"（即几乎整个日期不确定），则过滤掉该记录
5. 合并EX数据集中的最大日期（TRTSDT和TRTEDT的最大值）
6. 取所有有效日期的最大值作为LSTALVDT
7. 应用截止日期：如果LSTALVDT > cutoffdate，则设置为cutoffdate
8. 特殊情况处理（在DTHDT处理后进行）：
   - 如果LSTALVDT为空但有SCRNFFL（即筛选失败），则使用RFICDT（知情同意日期）
   - 如果有死亡记录且有非完全缺失的死亡日期，则使用DTHDT
   - LSTALVDT依旧为空，则使用RANDDT/ENRLDT

### DTHDT (死亡日期-数值)生成逻辑：

1. 从DTHDTC（字符型死亡日期）拆分出年、月、日部分

2. 对不完整日期进行推算：
   - 若缺失月份且死亡年份与LSTALVDT年份相同：使用LSTALVDT
   - 若缺失月份且死亡年份与LSTALVDT不同：使用该年的1月1日
   - 若缺失日期且死亡年月与LSTALVDT相同：使用LSTALVDT
   - 若缺失日期且死亡年月与LSTALVDT不同：使用该月的第1天
   - 若有完整日期：直接使用完整日期

3. 应用截止日期：如果DTHDT > cutoffdate，则设置为空值(NA)，并同时将DTHFL设置为空值(NA)

### 处理顺序：
   - 首先生成LSTALVDT（过滤无效日期、日期填补、cutoff）
   - 然后生成DTHDT（使用LSTALVDT进行日期填补，cutoff）
   - 最后再次更新LSTALVDT：如果有死亡记录且有非完全缺失的死亡日期（即不缺失DTHDT），则使用DTHDT

## 代码限制和注意事项

1. 这个函数依赖于特定的数据结构和变量命名规则
2. 一些变量的派生规则可能因研究设计而异
3. 部分变量派生依赖于特定的数据集命名模式（如以"EX"、"DSEOT"开头的数据集）
4. 函数中有大量的条件判断来处理不同情况下的数据缺失
5. 对于部分日期（如死亡日期）有特定的推算规则
6. 开放标签和盲法试验对某些变量的处理略有不同（例如TRT01P/TRT01A）
7. 处理多个EOT相关的变量时，使用了数值后缀来区分不同的EOT记录（可能和EDC数据集中EOT标记不同） 