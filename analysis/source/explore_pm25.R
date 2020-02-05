
rm(list=ls()) 

library(readr)
library(tidyverse)
library(snakecase)
library(lubridate)
library(ggplot2)
library(gridExtra)

#need to re-work so that the one-station dfs are saved...maybe not anymore...?
#plot all of the stations 

setwd("~/Documents/GitHub/final_project/analysis")
#make_path <- is_git_root$make_fix_file() #can't use, is_git_root???
#config <- yaml.load_file(make_path("analysis/config.yml"))
#out_path <- make_path(config$build_path)
out_path <- "~/Documents/GitHub/final_project/analysis/build"

pm25_chicago <- read_csv("~/Documents/GitHub/final_project/data/pm25/pm25_chicago_2010.csv") %>%
  set_names(to_snake_case(colnames(.))) %>%
  mutate(date = mdy(date))


#bar plot of the avg pm25 overy the year at ea site
pm25_chicago %>%
  group_by(site_name)%>%
  summarize(mean_pm25 = mean(daily_mean_pm_2_5_concentration)) %>%
  ggplot(aes(x = site_name, y =  mean_pm25))+
    geom_bar(stat = "identity")

#line plot of avg monthly pm25 for a single station
plot_month_pm25 <- function(xi, s_name){
  one_site <- pm25_chicago%>%
    filter(site_id == xi)

  one_site %>%
    group_by(month=floor_date(date, "month")) %>%
    #https://ro-che.info/articles/2017-02-22-group_by_month_r
    summarize(mean_pm25 = mean(daily_mean_pm_2_5_concentration)) %>%
  ggplot() +
    geom_line(aes(x=month, y = mean_pm25))+
    labs(title = s_name)
}


p1 <- plot_month_pm25(170310052,"MAYFAIR PUMP STATION")

p2<- plot_month_pm25(170310057, "SPRINGFIELD PUMP STATION")

p3 <- plot_month_pm25(170311016, "VILLAGE HALL")

p4 <- plot_month_pm25(181270024, "Ogden Dunes- Water Treatment Plant")

#plot_month_pm25(550590019, "CHIWAUKEE PRAIRIE STATELINE")

plot <- grid.arrange(p1,p2,p3,p4)

ggsave("seasonality_top_4_pm25_stations.png", plot, path = out_path)


site_ids <- data.frame(unique(pm25_chicago$site_id))  #should put in a fn to clean the envi....
plot_list <- c()
myplots <- vector('list', ncol(pm25_chicago)) #not sure about the length arg

#myplots <- lapply(colnames(pm25_chicago$site_id), plot_month_pm25, data = pm25_chicago)

#site_ids[3,1]


for (i in 1:2){
  #plot_i <- plot_month_pm25(site_id[i,1], i)
  #plot_month_pm25(site_ids[i,1], i) #whoops, uncommented wrong one!
  #append(plot_list, plot_i) 
  myplots[[i]] <- local({
    pi <- plot_month_pm25(site_ids[i,1], site_ids[i,1])
    print(pi)
  })
}
plot_i
#https://stackoverflow.com/questions/31993704/storing-ggplot-objects-in-a-list-from-within-loop-in-r

p <- list()
for(i in 1:30){
  p[[i]] <- plot_month_pm25(site_ids[i,1], site_ids[i,1])
}
big_plot <- do.call(grid.arrange,p)

ggsave("seasonality_pm25_stations_all.png", big_plot, path = out_path)






#doesn't work
regn_month_pm25 <- function(xi){
  one_site <- pm25_chicago%>%
    filter(site_id == xi)
  one_site %>%
    group_by(month=floor_date(date, "month")) %>%
    #https://ro-che.info/articles/2017-02-22-group_by_month_r
    summarize(mean_pm25 = mean(daily_mean_pm_2_5_concentration)) %>%
    
    lin_model <- lm(mean_pm25~month)
    summary(lin_model)
}
regn_month_pm25(181270024)

  
m <- lm(daily_mean_pm_2_5_concentration~date, data = pm25_chicago)
summary(m)
  
  
  
  