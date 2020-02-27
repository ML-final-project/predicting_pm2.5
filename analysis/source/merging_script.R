library(yaml)
library(rprojroot)
library(tidyverse)
library(lubridate)
library(snakecase)
library(sf)
library(plm)

setwd("~/final_project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)
data_out <- make_path(config$data_path$merge)
source(str_c(config$group_code, "prelim.R"))

noaa <- read_csv(make_path(config$data_path$noaa,
                           "Chicago2010Daily.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  select(station_name,
         date,
         elevation,
         latitude,
         longitude,
         contains("normal")) %>%
  na_if(-9999) %>%
  na.omit() %>%
  mutate(date = ymd(date)) %>%
  st_as_sf(coords = c("longitude", "latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km")
# dropping missing data - hopefully there is no selection bias

pm25 <- read_csv(make_path(config$data_path$pm25,
                           "pm25_chicago_2010.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  mutate(date = mdy(date)) %>%
  st_as_sf(coords = c("site_longitude", "site_latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km") %>%
  na.omit() %>%
  select(date, site_name, daily_mean_pm_2_5_concentration)

pm25_sites <- distinct(pm25, site_name)
noaa_sites <- distinct(noaa, station_name)

min.col <- function(m, ...) max.col(-m, ...)
pm25_sites$row_num <- st_distance(pm25_sites, noaa_sites) %>% min.col(.)

sites <- noaa_sites %>%
  mutate(row_num = row_number()) %>%
  st_set_geometry(NULL) %>%
  right_join(., pm25_sites, by = "row_num") %>%
  select(-c(row_num, geometry))

merged <- pm25 %>%
  left_join(., sites, by = "site_name") %>%
  st_set_geometry(NULL) %>%
  left_join(., noaa, by = c("station_name","date")) %>%
  select(-geometry)
write.csv(merged, str_c(data_out, "/merged_noaa_pm25.csv"))

##############
## aod data ##
##############

aod_047 <- read_csv(make_path(config$data_path$aod,
                              "2010ImputedOpticalDepth_047nm.csv"),
                    col_names = FALSE) %>%
  rename(date = X1,
         aod47 = X2)

aod_055 <- read_csv(make_path(config$data_path$aod,
                              "2010ImputedOpticalDepth_055nm.csv"),
                    col_names = FALSE) %>%
  rename(date = X1,
         aod55 = X2)

merged_aod <- left_join(aod_047, aod_055, by = "date") %>%
  right_join(., merged, by = "date")
write.csv(merged_aod, str_c(data_out, "/merged_noaa_pm25_aod.csv"))

#######################
## linear regression ##
#######################

reg_vars <- merged_aod %>%
  select(elevation, contains("normal"), aod47, aod55) %>%
  names() %>%
  paste(collapse = " + ")

summary(plm(as.formula(paste0("daily_mean_pm_2_5_concentration ~ ", reg_vars)),
            data = merged_aod,
            index = c("date"),
            model = "within",
            effect = "twoways"))
