# xpt导出&读取

### R输出xpt
```R
library(haven)
write_xpt(adam_data$ADAE, tmp, version = 5,name="ALL")
## version = 5 or 8
## name="ALL" 必须使用，否则r会自定义一个名字，导致读入sas困难 
```

### SAS读入xpt
```SAS
libname xptin xport  "C:\Users\wangjy35\Downloads\test\xpt\adae.xpt";
libname datasets 'C:\Users\wangjy35\Downloads\test\data';

proc copy in=xptin out=datasets;
run;
```