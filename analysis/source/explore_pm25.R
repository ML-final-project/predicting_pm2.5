library(readr)
library(tidyverse)
library(snakecase)
library(lubridate)
library(ggplot2)
library(gridExtra)

setwd("~/Documents/GitHub/final_project/analysis")


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

grid.arrange(p1,p2,p3,p4)


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
  
  
  
  