# ADAE数据集生成规则文档 

## 功能概述

`gen_adae`函数的主要功能是根据原始EDC数据和规范(spec)生成ADAE(Analysis Data Adverse Events，分析用途的不良事件数据集)数据集。这个数据集包含临床试验中各受试者所有不良事件的详细信息，如不良事件内容、编码信息、严重程度、发生日期、关联性等。

## 函数参数

- `data`: 原始数据列表，包含多个数据框
- `spec`: ADAE相关的JSON规范列表
- `adsl`: ADSL数据框，提供受试者基础信息
- `aftrtedt`: 治疗期间不良事件(TEAE)的判断标准，非肿瘤设置为F，肿瘤设置为T
- `lagdy`: TEAE的判断标准，肿瘤设置：AESTDT <= TRTEDT + lagdy
- `cutoffdate`: 主要的数据截止日期

## 输入和输出

- **输入**: 原始EDC数据、JSON规范和ADSL数据集
- **输出**: 包含规范中要求的所有变量的ADAE数据框

## 处理流程

该函数的处理流程分为几个主要步骤：

1. **提取依赖关系信息**: 从规范中提取原始数据和ADAM数据的依赖关系
2. **数据获取和合并**: 从不同数据集中获取所需变量，特别处理AEACNx和AERELx变量
3. **日期处理**: 对不良事件开始日期(AESTDT)进行缺失值填补
4. **TEAE标志生成**: 根据参数确定治疗期间不良事件标志(TRTEMFL)
5. **关联性分组**: 生成不良事件与试验药物关联性分组变量(RELGR1和RELGR1N)
6. **类型转换**: 处理变量类型和格式转换
7. **数据截止处理**: 根据截止日期处理数据
8. **标签设置**: 设置变量标签
9. **返回结果**: 返回最终的ADAE数据集

## 变量生成规则

### 基本信息变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| STUDYID | 研究标识符 | 从AE.STUDYCODE或AE.STUDYID获取 |
| SUBJID | 研究中的受试者标识符 | 从AE.SUBJID获取<br>匹配AE编码文件变量：Subject Code |
| AESPID | 受赞助者定义的标识符 | AE.SN的数值版本<br>匹配AE编码文件变量：Sn |

### 不良事件描述变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AETERM | 报告术语 | 从AE.AETERM获取<br>匹配AE编码文件变量：Verbatims |
| AEDECOD_CN | 字典派生术语（中文） | 从AE_CODING.PT_CN获取 |
| AEDECOD_EN | 字典派生术语（英文） | 从AE_CODING.PT_EN获取 |
| AEPTCD | 首选术语代码 | 从AE_CODING.PT Code获取 |
| AEBODSYS_CN | 身体系统或器官分类（中文） | 从AE_CODING.SOC_CN获取<br>**注意**: 实际实现中等于AESOC_CN |
| AEBODSYS_EN | 身体系统或器官分类（英文） | 从AE_CODING.SOC_EN获取<br>**注意**: 实际实现中等于AESOC_EN |
| AEBDSYCD | 身体系统或器官分类代码 | 从AE_CODING.SOC Code获取<br>**注意**: 实际实现中等于AESOCCD |
| AELLT_CN | 最低级术语（中文） | 从AE_CODING.LLT_CN获取 |
| AELLT_EN | 最低级术语（英文） | 从AE_CODING.LLT_EN获取 |
| AELLTCD | 最低级术语代码 | 从AE_CODING.LLT Code获取 |
| AESOC_CN | 主要系统器官分类（中文） | 从AE_CODING.SOC_CN获取 |
| AESOC_EN | 主要系统器官分类（英文） | 从AE_CODING.SOC_EN获取 |
| AESOCCD | 主要系统器官分类代码 | 从AE_CODING.SOC Code获取 |

### 日期变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AESTDTC | 观察开始日期/时间 | 从AE.AESTDAT获取 |
| AEENDTC | 观察结束日期/时间 | 从AE.AEENDAT获取 |
| AESTDT | 观察开始日期/时间 | 对AE.AESTDAT进行缺失值填补：<br>1. 完全缺失 = TRTSDT<br>2. 如果月份缺失但年份与TRTSDT相同：使用TRTSDT，否则使用该年的1月1日<br>3. 如果日期缺失但年月与TRTSDT相同：使用TRTSDT，否则使用该月的第1天<br>4. 如果有完整日期：直接使用完整日期 |

### 分析标志变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| TRTEMFL | 治疗期间不良事件分析标志 | 根据参数设置：<br>- 当aftrtedt=T时：如果AESTDT >= TRTSDT且AESTDT <= TRTEDT + lagdy，则为"Y"<br>- 当aftrtedt=F时：如果AESTDT >= TRTSDT，则为"Y" |

### 处理和关联性变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AEACNx | 对研究治疗采取的措施x | 从AE.AEACNx获取<br>**注意**: 支持多个AEACNx变量，通过starts_with()函数获取 |
| AERELx | 因果关系x | 从AE.AERELx获取<br>**注意**: 支持多个AERELx变量，通过starts_with()函数获取 |
| RELGR1 | 汇总因果关系组1 | 如果任一AERELx包含以下任一值，则为"RELATED"：<br>**老项目**: "Related"/"肯定有关"、"Possibly Related"/"可能有关"、"Unassessable"/"无法判定"<br>**新项目五分法**: "Definitely Related"/"肯定有关"、"很可能有关"、"Probably Related"、"Possibly Related"/"可能有关"<br>否则为"UNRELATED"<br>**注意**: 缺失值会作为UNRELATED处理 |
| RELGR1N | 汇总因果关系组1（数值） | 如果RELGR1为"RELATED"，则为1；如果为"UNRELATED"，则为0 |

### 严重性和特征变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AESER | 严重事件 | 如果AE.AESER为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESCONG | 先天性异常或出生缺陷 | 如果AE.AESCONG为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESDISAB | 持续或显著残疾/丧失能力 | 如果AE.AESDISAB为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESDTH | 导致死亡 | 如果AE.AESDTH为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESHOSP | 需要或延长住院 | 如果AE.AESHOSP为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESLIFE | 危及生命 | 如果AE.AESLIFE为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESMIE | 其他医学上重要的严重事件 | 如果AE.AESMIE为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AETOXGR | 标准毒性等级 | 从AE.AETOXGR获取，并转换为字符型 |
| AESEV | 严重程度 | 从AE.AESEV获取 |
| AEOUT | 不良事件结局 | 从AE.AEOUT获取 |

### 特殊兴趣变量

| 变量名 | 描述 | 生成规则 |
|--------|------|----------|
| AEDIS | 因不良事件而停药 | 如果AE.AEDIS为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AESI | 特别关注的事件 | 如果AE.AESI为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AEDLT | 剂量限制性毒性 | 如果AE.AEDLT为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |
| AEIRAE | 免疫相关不良事件 | 如果AE.AEIRAE为"Yes"/"是"则为"Y"，"No"/"否"则为"N" |

## 数据截取处理

根据传入的cutoffdate参数，对ADAE数据进行如下处理：

1. 过滤掉AESTDT > cutoffdate的记录
2. 当AEENDTC > cutoffdate时：
   - 如果AEOUT为"Fatal"/"死亡"、"Recovered/Resolved"/"恢复/解决"、"Recovered/Resolved with Sequelae"/"恢复/解决有后遗症" 、"Recovering/Resolving"/"恢复中"、"Unknown"/"未知"值，则修改为"Not Recovered/Not Resolved"/"未恢复/未解决"
   - 将AEENDTC设置为空值(NA)

## 代码限制和注意事项

1. 函数依赖于特定的数据结构和变量命名规则
2. 某些不良事件处理逻辑（如TEAE的判定）可能因研究类型（肿瘤/非肿瘤）而异
3. AEACNx和AERELx变量支持多个治疗相关的措施和因果关系评估
4. 关联性变量RELGR1的处理与常规不同，缺失值会被归为"UNRELATED"类别
5. 该函数要求提供ADSL数据集作为参数，用于获取受试者的治疗信息（TRTSDT、TRTEDT等） 