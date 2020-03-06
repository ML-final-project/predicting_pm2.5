rm(list=ls())

library(dbplyr)
library(finalfit)

setwd("~/Documents/GitHub/final_project")
#setwd("~/final_project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)
data_out <- make_path(config$data_path$merge)


noaa <- read_csv(make_path(config$data_path$noaa,
                           "Chicago2010Daily.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  select(station_name,
         date,
         elevation,
         latitude,
         longitude,
         contains("normal")) %>%
  na_if(-9999)

#no pm25 missing
#pm25 <- read_csv(make_path(config$data_path$pm25,
#                           "pm25_chicago_2010.csv")) %>%
 # set_names(to_snake_case(colnames(.))) %>%
  #mutate(date = mdy(date)) %>%
  #st_as_sf(coords = c("site_longitude", "site_latitude"),
  #         crs = 4326, remove = FALSE) %>%
  #st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km") %>%
  #select(date, site_name, daily_mean_pm_2_5_concentration)


noaa %>%
  missing_plot()

noaa$missing_tmin = ifelse(is.na(noaa$dly_tmin_normal), 1, 0)

t.test(noaa$missing_tmin)


