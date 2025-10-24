# R结合AI的用法 & 参考网址

## 相关package

#### {ellmer}: 提供各大AI调用模式  
https://ellmer.tidyverse.org/index.html

#### {shinychat}: shiny ai聊天框 
https://posit-dev.github.io/shinychat/r/index.html

## 教程

#### R Sidebot: How to Add an LLM Assistant to Your R Shiny Apps
https://www.appsilon.com/post/r-sidebot

## 我用ai写的

``` r

# 数据导航器 - AI 助手（改进版 V2）
# 增加手动执行按钮，确保代码能被执行

library(shiny)
library(shinychat)
library(ellmer)
library(dplyr)
library(DT)
library(bslib)

dp_url = 
dp_apikey = 

# 解决包冲突
if (requireNamespace("conflicted", quietly = TRUE)) {
  library(conflicted)
  conflicts_prefer(shiny::actionButton)
  conflicts_prefer(dplyr::filter)
  conflicts_prefer(dplyr::lag)
}

# 示例数据集
demo_data <- data.frame(
  USUBJID = sprintf("S-%02d-%04d", rep(1:3, each = 10), 1:30),
  SEX = sample(c("M", "F"), 30, replace = TRUE),
  RACE = sample(c("White", "Black", "Asian"), 30, replace = TRUE),
  ARM = sample(c("Placebo", "Treatment A", "Treatment B"), 30, replace = TRUE),
  AGE = round(rnorm(30, mean = 45, sd = 12)),
  WEIGHT = round(rnorm(30, mean = 70, sd = 15), 1),
  HEIGHT = round(rnorm(30, mean = 170, sd = 10), 1),
  COUNTRY = sample(c("USA", "Canada", "UK"), 30, replace = TRUE),
  VISIT = sample(1:5, 30, replace = TRUE),
  stringsAsFactors = FALSE
)

# 系统提示词
system_prompt <- paste(
  "你是一个 R 语言数据分析助手。用户会用自然语言描述数据操作需求。",
  "你需要：",
  "1. 理解用户的需求",
  "2. 生成相应的 R 代码（使用 dplyr 语法）",
  "3. 代码应该对名为 'data' 的数据框进行操作",
  "4. 只返回可以直接执行的 R 代码，用 ```r 代码块包裹",
  "5. 在代码前用中文简短说明你的理解",
  "",
  "数据框列名：", paste(names(demo_data), collapse = ", "),
  "",
  "示例：",
  "用户：筛选年龄大于平均值的受试者",
  "助手：我会筛选年龄大于平均年龄的所有受试者。",
  "```r",
  "data %>% filter(AGE > mean(AGE, na.rm = TRUE))",
  "```"
)

ui <- page_sidebar(
  title = "数据导航器 - AI 助手",
  theme = bs_theme(
    version = 5,
    preset = "shiny",
    primary = "#00A5E5",
    font_scale = 0.9
  ),
  
  sidebar = sidebar(
    width = 480,
    h4("AI 助手", style = "margin-top: 0;"),
    p("用自然语言查询数据，AI 会生成代码。", 
      style = "font-size: 0.9em; color: #666;"),
    
    # 聊天界面
    chat_ui(
      id = "chat",
      messages = "**你好！** 我是数据分析助手。请告诉我你想如何处理数据。",
      height = "calc(100vh - 350px)"
    ),
    
    # 代码输入框（用于粘贴 AI 生成的代码）
    div(
      style = "margin-top: 10px; margin-bottom: 10px;",
      textAreaInput(
        "manual_code",
        "AI 生成的代码（自动提取或手动粘贴）：",
        placeholder = "data %>% filter(AGE > 50)",
        rows = 3,
        width = "100%"
      )
    ),
    
    hr(),
    
    div(
      style = "display: grid; grid-template-columns: 1fr 1fr; gap: 10px;",
      actionButton("execute_code", "执行代码", icon = icon("play"), class = "btn-success btn-sm"),
      actionButton("reset_data", "重置数据", icon = icon("undo"), class = "btn-secondary btn-sm")
    )
  ),
  
  # 主内容区
  navset_card_tab(
    nav_panel(
      "数据表",
      card_body(
        div(
          style = "display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;",
          p(
            strong("当前数据："), 
            textOutput("data_summary", inline = TRUE),
            style = "margin: 0;"
          )
        ),
        DTOutput("data_table")
      )
    ),
    nav_panel(
      "执行历史",
      card_body(
        uiOutput("execution_history")
      )
    ),
    nav_panel(
      "关于",
      card_body(
        h4("使用说明"),
        tags$ol(
          tags$li("在左侧聊天框输入自然语言查询，例如：\"筛选年龄大于 50 的受试者\""),
          tags$li("AI 会生成相应的 R 代码"),
          tags$li("代码会自动提取到代码输入框（或手动复制粘贴）"),
          tags$li(strong("点击\"执行代码\"按钮"), "来运行代码并更新数据表")
        ),
        h4("示例查询", class = "mt-4"),
        tags$ul(
          tags$li("筛选年龄大于 50 的受试者"),
          tags$li("显示安慰剂组中的白人男性"),
          tags$li("按年龄降序排列"),
          tags$li("显示体重大于 70kg 的女性受试者"),
          tags$li("筛选来自美国的治疗组受试者")
        )
      )
    )
  )
)

server <- function(input, output, session) {
  
  # 存储当前数据
  current_data <- reactiveVal(demo_data)
  
  # 存储执行历史
  execution_log <- reactiveVal(list())
  
  # 存储用户查询
  last_user_query <- reactiveVal("")
  
  # 存储最新的AI响应内容
  last_ai_response <- reactiveVal("")
  
  # 创建 DeepSeek 聊天对象
  chat <- chat_deepseek(
    system_prompt = system_prompt,
    base_url = dp_url,
    api_key = dp_apikey,
    model = "DeepSeek-R1"
  )
  
  # 提取 R 代码
  extract_r_code <- function(text) {
    if (is.null(text) || trimws(text) == "") return(NULL)
    
    # 匹配 ```r 或 ```R 代码块
    patterns <- c(
      "```r\\s*\\n([^`]+)```",
      "```R\\s*\\n([^`]+)```"
    )
    
    for (pattern in patterns) {
      matches <- regmatches(text, gregexpr(pattern, text, perl = TRUE))
      
      if (length(matches[[1]]) > 0) {
        code <- matches[[1]][1]
        code <- gsub("```[rR]\\s*\\n", "", code, perl = TRUE)
        code <- gsub("```$", "", code)
        code <- trimws(code)
        if (nchar(code) > 0) return(code)
      }
    }
    
    return(NULL)
  }
  
  # 安全执行代码
  safely_execute_code <- function(code, data) {
    if (is.null(code) || trimws(code) == "") {
      return(list(success = FALSE, error = "代码为空"))
    }
    
    tryCatch({
      env <- new.env()
      env$data <- data
      
      # 在执行环境中加载 dplyr 函数，避免冲突
      env$filter <- dplyr::filter
      env$select <- dplyr::select
      env$mutate <- dplyr::mutate
      env$arrange <- dplyr::arrange
      env$summarise <- dplyr::summarise
      env$group_by <- dplyr::group_by
      env$`%>%` <- dplyr::`%>%`
      
      result <- eval(parse(text = code), envir = env)
      
      if (!is.data.frame(result)) {
        return(list(success = FALSE, error = "结果不是数据框"))
      }
      
      if (nrow(result) == 0) {
        return(list(success = FALSE, error = "结果为空数据框（没有匹配的记录）"))
      }
      
      list(success = TRUE, data = result)
    }, error = function(e) {
      list(success = FALSE, error = e$message)
    })
  }
  
  # 监听用户输入
  observeEvent(input$chat_user_input, {
    req(input$chat_user_input)
    
    user_msg <- input$chat_user_input
    last_user_query(user_msg)
    
    # 显示加载提示
    showNotification(
      "AI 正在生成代码...",
      type = "message",
      duration = 2,
      id = "ai_loading"
    )
    
    # 使用同步响应以便获取完整文本
    tryCatch({
      # 获取AI响应
      response <- chat$chat(user_msg)
      
      # 保存响应文本
      response_text <- as.character(response)
      last_ai_response(response_text)
      
      # 添加到聊天界面
      chat_append("chat", response_text)
      
      # 尝试提取代码
      extracted_code <- extract_r_code(response_text)
      
      if (!is.null(extracted_code)) {
        # 自动填充到代码输入框
        updateTextAreaInput(session, "manual_code", value = extracted_code)
        
        showNotification(
          "✓ 已自动提取代码到输入框，请检查后点击\"执行代码\"",
          type = "message",
          duration = 4
        )
      } else {
        showNotification(
          "AI 已回复，但未检测到代码块，请手动复制粘贴",
          type = "warning",
          duration = 4
        )
      }
    }, error = function(e) {
      showNotification(
        paste("AI 响应错误:", e$message),
        type = "error",
        duration = 5
      )
    })
  })
  
  # 手动执行代码
  observeEvent(input$execute_code, {
    code <- trimws(input$manual_code)
    
    if (code == "") {
      showNotification("请先输入或粘贴代码", type = "warning")
      return()
    }
    
    # 如果代码包含 ```r，提取纯代码
    extracted_code <- extract_r_code(code)
    if (!is.null(extracted_code)) {
      code <- extracted_code
    }
    
    # 执行代码
    result <- safely_execute_code(code, current_data())
    
    if (result$success) {
      current_data(result$data)
      
      # 记录成功
      log_entry <- list(
        timestamp = Sys.time(),
        query = last_user_query(),
        code = code,
        success = TRUE,
        rows = nrow(result$data)
      )
      execution_log(c(execution_log(), list(log_entry)))
      
      showNotification(
        paste("✓ 执行成功！当前", nrow(result$data), "行数据"),
        type = "message",
        duration = 3
      )
    } else {
      # 记录失败
      log_entry <- list(
        timestamp = Sys.time(),
        query = last_user_query(),
        code = code,
        success = FALSE,
        error = result$error
      )
      execution_log(c(execution_log(), list(log_entry)))
      
      showNotification(
        paste("✗ 执行失败：", result$error),
        type = "error",
        duration = 5
      )
    }
  })
  
  # 显示数据表
  output$data_table <- renderDT({
    datatable(
      current_data(),
      options = list(
        pageLength = 15,
        scrollX = TRUE,
        dom = 'Bfrtip',
        buttons = c('copy', 'csv', 'excel'),
        language = list(
          search = "搜索",
          lengthMenu = "显示 _MENU_ 条记录",
          info = "显示 _START_ 到 _END_ 条，共 _TOTAL_ 条记录",
          paginate = list(
            first = "首页",
            last = "末页",
            'next' = "下一页",
            previous = "上一页"
          )
        )
      ),
      class = "display nowrap compact",
      rownames = FALSE
    )
  })
  
  # 数据摘要
  output$data_summary <- renderText({
    sprintf("%d 行 × %d 列", nrow(current_data()), ncol(current_data()))
  })
  
  # 执行历史
  output$execution_history <- renderUI({
    logs <- execution_log()
    
    if (length(logs) == 0) {
      return(div(
        style = "text-align: center; color: #999; padding: 40px;",
        icon("history", style = "font-size: 4em; margin-bottom: 15px; opacity: 0.5;"),
        h5("暂无执行历史"),
        p("开始与 AI 对话，然后点击\"执行代码\"按钮。")
      ))
    }
    
    items <- lapply(rev(logs), function(log) {
      # 判断是否为重置操作
      is_reset <- !is.null(log$is_reset) && log$is_reset
      
      status_badge <- if (is_reset) {
        span(class = "badge bg-info", icon("undo"), " 重置")
      } else if (log$success) {
        span(class = "badge bg-success", icon("check"), " 成功")
      } else {
        span(class = "badge bg-danger", icon("times"), " 失败")
      }
      
      card(
        card_header(
          div(
            style = "display: flex; justify-content: space-between; align-items: center;",
            span(
              icon("clock"),
              " ",
              format(log$timestamp, "%H:%M:%S")
            ),
            status_badge
          )
        ),
        card_body(
          div(
            strong(icon(if(is_reset) "undo" else "comment"), 
                   if(is_reset) " 操作：" else " 查询："),
            p(log$query, style = "margin-left: 20px; font-style: italic;")
          ),
          if (!is_reset) {
            div(
              strong(icon("code"), " 代码："),
              tags$pre(
                style = "background: #f5f5f5; padding: 10px; border-radius: 4px; overflow-x: auto; margin-left: 20px;",
                tags$code(log$code)
              )
            )
          } else {
            div(
              strong(icon("info-circle"), " 说明："),
              p("数据已恢复到初始状态", 
                style = "margin-left: 20px; color: #0288d1;")
            )
          },
          if (log$success) {
            div(
              strong(icon("table"), " 结果："),
              p(sprintf(if(is_reset) "已重置，共 %d 行数据" else "成功筛选，当前 %d 行数据", log$rows), 
                style = paste0("margin-left: 20px; color: ", if(is_reset) "#0288d1;" else "green;"))
            )
          } else {
            div(
              strong(icon("exclamation-triangle"), " 错误："),
              div(
                style = "background: #ffe6e6; padding: 10px; border-radius: 4px; color: #d32f2f; margin-left: 20px;",
                log$error
              )
            )
          }
        )
      )
    })
    
    tagList(items)
  })
  
  # 重置数据
  observeEvent(input$reset_data, {
    current_data(demo_data)
    
    # 记录重置操作
    log_entry <- list(
      timestamp = Sys.time(),
      query = "重置数据",
      code = "# 数据已重置到初始状态",
      success = TRUE,
      rows = nrow(demo_data),
      is_reset = TRUE  # 标记为重置操作
    )
    execution_log(c(execution_log(), list(log_entry)))
    
    showNotification("✓ 数据已重置到初始状态", type = "message")
  })
}

shinyApp(ui, server)

```