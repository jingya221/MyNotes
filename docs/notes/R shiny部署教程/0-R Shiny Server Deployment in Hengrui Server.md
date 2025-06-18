# R Shiny Server Deployment in Hengrui Server

## Server Info

```` 
shnvlshiny01	10.10.5.114	 root/Hr@shiny0821        
shnvlshinyd01	10.10.13.56  root/Hr@shiny0821
````

## Steps
* shiny-server guide: https://docs.posit.co/shiny-server/
* IT grant access to https://cran.rstudio.com/
* yum install R
* su - -c "R -e \"install.packages(c('shiny', 'rmarkdown', 'devtools', 'RJDBC'), repos='https://cran.rstudio.com/')\""
* Download Shiny Server: https://posit.co/download/shiny-server/
* yum install --nogpgcheck shiny-server-1.5.20.1002-x86_64.rpm
* systemctl start shiny-server
* systemctl enable shiny-server

## Shiny Server Info

* site_dir: **/srv/shiny-server**
* log_dir: **/var/log/shiny-server**
* config_dir: **/etc/shiny-server/shiny-server.conf**

## Install prerequisite apps for R packages

yum install harfbuzz-devel fribidi-devel
yum install freetype-devel libpng-devel libtiff-devel libjpeg-turbo-devel
yum install poppler-cpp-devel

yum install libcurl-devel libxml2-devel openssl-devel libgit2-devel

## Install R packages

````
su - -c "R -e \"install.packages(c('shiny', 'rmarkdown', 'devtools', 'RJDBC'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('DT'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('readxl'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('RSQLite'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('DBI'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('shinyjs'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('shinyWidgets'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('bslib'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('shinydisconnect'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('openxlsx'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('pdftools'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('shinyalert'), repos='https://cran.rstudio.com/')\""
su - -c "R -e \"install.packages(c('tidyverse'), repos='https://cran.rstudio.com/')\""

su - -c "R -e \"install.packages(c('config','golem'), repos='https://cran.rstudio.com/')\""
````

## Deploy Shiny Apps

Save app folder in **/srv/shiny-server**, should have two files, **ui.r** and **server.r**

## Deploy with golem

https://github.com/ThinkR-open/golem/issues/145

![image-20231121155457291](C:\Users\quyd\AppData\Roaming\Typora\typora-user-images\image-20231121155457291.png)

Install the package create by `golem`.

````r
install.packages('/tmp/systemd-private-36b2a1fdf86c4a96acd80d08f2d0342c-chronyd.service-7hjinM/tmp/DefineHelper_1.0.tar.gz',lib = .libPaths()[length(.libPaths())],repos = NULL,dependencies = T)
````



Create a `app.r` file within the app folder, i.e. ` **/srv/shiny-server/define-helper**`. Note that `app.r` must be saved with UTF-8 encoding

Sample `app.r` file:

```` r
options(shiny.maxRequestSize = 100*1024^2) #setting upload limit to 100MB
DefineHelper::run_app()
````



## Add-on

Grant write access right to /srv/shiny-server, for the upload file of Shiny App

```` shell
sudo chmod -R 777 define-helper
````

need investigation on how to configure a different location, such as /tmp/ for upload files, in *server* function of shiny app.



## Emacs

quit: Ctrl-x Ctrl-c

save: Crtl-x Ctrl-s

## R Shiny Configuration files

```` 
# Instruct Shiny Server to run applications as the user "shiny"
run_as shiny;
preserve_logs true;

# Define a server that listens on port 80
server {
  listen 80; 

  # Define a location at the base URL
  location / {

    # Host the directory of Shiny Apps stored in this directory
    site_dir /srv/shiny-server;

    # Log all Shiny output to files in this directory
    log_dir /var/log/shiny-server;

    # When a user visits the base URL rather than a particular application,
    # an index of the applications available in this directory will be shown.
    directory_index on;
  }
}
````

## Https link

https://shinyapp.hengrui.com/

## Other mirrors of R packages

https://cran.r-project.org/
https://cloud.r-project.org/
https://mirrors.tuna.tsinghua.edu.cn/CRAN/
https://mirrors.aliyun.com/CRAN/

# Reference

**netstat -lnpt**