library(yaml)
library(rprojroot)
library(tidyverse)
library(lubridate)
library(snakecase)
library(sf)

setwd("~/final_project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)
source(str_c(config$group_code, "prelim.R"))

noaa <- read_csv(make_path(config$data_path$noaa,
                           "Chicago2010Data.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  st_as_sf(coords = c("longitude", "latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km")

pm25 <- read_csv(make_path(config$data_path$pm25,
                           "pm25_chicago_2010.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  st_as_sf(coords = c("site_longitude", "site_latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km") %>%
  st_buffer(15) # 15km

pm25_avrg <- pm25 %>%
  mutate(date = mdy(date)) %>%
  mutate(month = floor_date(date, unit = "month")) %>%
  group_by(month, site_name) %>%
  summarise(monthly_average = mean(daily_mean_pm_2_5_concentration)) %>%
  separate(month, into = c("rm", "month", "rm1"), sep = "-") %>%
  select(-c(rm, rm1))

ggplot() +
  geom_sf(data = pm25_avrg,
          color = 'red') +
  geom_sf(data = noaa,
          color = 'blue') +
  theme(
    legend.position="none",
    line = element_blank(),
    rect = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid.major = element_line(colour = "transparent")
  )
ggsave("pmg25_noaa_buffer.png", plot = last_plot(), path = out_path)

intersections <- st_intersection(pm25_avrg, noaa)
