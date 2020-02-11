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

aod_047 <- read_csv(make_path(config$data_path$aod,
                              "ChicagoOpticalDepth2010_047nm_line.csv"),
                    skip = 7) %>%
  rename(date = `\\f0\\fs24 \\cf0 date`,
         aod_47 = `value_`,
         county = `county\\`) %>%
  na.omit() %>%
  mutate(county = "Cook") %>%
  group_by(date) %>%
  mutate(aod_47 = mean(aod_47))

min.col <- function(m, ...) max.col(-m, ...)
pm25$closest <- st_distance(pm25, noaa) %>% min.col(.)

merged <- pm25 %>%
  left_join(
    noaa %>% mutate(row_num = row_number()) %>% st_set_geometry(NULL),
    by = c("closest" = "row_num"), "date")

reg_vars <- merged %>%
  select(elevation, contains("normal")) %>%
  st_set_geometry(NULL) %>%
  names() %>%
  paste(collapse = " + ")

summary(plm(as.formula(paste0("daily_mean_pm_2_5_concentration ~ ",
                              reg_vars)),
            data = merged,
            index = c("date.x"),
            model = "within",
            effect = "twoways"))
write.csv(merged, str_c(data_out, "/merged_noaa_pm25.csv"))

##############
## aod data ##
##############

aod_047 <- read_csv(make_path(config$data_path$aod,
                              "ChicagoOpticalDepth2010_047nm_line.csv"),
                    skip = 7) %>%
  rename(date = `\\f0\\fs24 \\cf0 date`,
         aod_47 = `value_`,
         county = `county\\`) %>%
  na.omit() %>%
  mutate(county = "Cook")

aod_055 <- read_csv(make_path(config$data_path$aod,
                              "ChicagoOpticalDepth2010_055nm_line.csv"),
                    skip = 7) %>%
  rename(date = `\\f0\\fs24 \\cf0 date`,
         aod_55 = `value_`,
         county = `county\\`) %>%
  na.omit() %>%
  mutate(county = "Cook")
