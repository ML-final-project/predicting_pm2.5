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
data_out <- make_path(config$data_path$merge)
source(str_c(config$group_code, "prelim.R"))

noaa <- read_csv(make_path(config$data_path$noaa,
                           "Mass2010Normal.csv")) %>%
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
  mutate(state = case_when(str_detect(station_name, "CA") ~ "CA",
                           str_detect(station_name, "IL") ~ "IL",
                           str_detect(station_name, "AK") ~ "AK",
                           str_detect(station_name, "CO") ~ "CO",
                           str_detect(station_name, "FL") ~ "FL")) %>%
  st_as_sf(coords = c("longitude", "latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km")

pm25_read <- tibble()
for (file in grep("?.csv",
                  list.files(make_path(config$data_path$pm25),
                             pattern = "*2010.csv"),
                  value = T)) {
  .tmp <- read_csv(make_path(config$data_path$pm25, file))
  pm25_read <- pm25_read %>% rbind(.tmp)
}

pm25 <- pm25_read %>%
  set_names(to_snake_case(colnames(.))) %>%
  mutate(date = mdy(date)) %>%
  st_as_sf(coords = c("site_longitude", "site_latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=utm +zone=42N +datum=WGS84 +units=km") %>%
  na.omit() %>%
  mutate(state = case_when(state == "California" ~ "CA",
                           state == "Illinois" ~ "IL",
                           state == "Alaska" ~ "AK",
                           state == "Colorado" ~ "CO",
                           state == "Florida" ~ "FL")) %>%
  select(date, site_name, daily_mean_pm_2_5_concentration, state)

pm25_sites <- distinct(pm25, site_name, state)
noaa_sites <- distinct(noaa, station_name, state)

min.col <- function(m, ...) max.col(-m, ...)
pm25_sites$row_num <- st_distance(pm25_sites, noaa_sites) %>% min.col(.)

sites <- noaa_sites %>%
  mutate(row_num = row_number()) %>%
  st_set_geometry(NULL) %>%
  select(-state) %>%
  right_join(., pm25_sites, by = "row_num") %>%
  select(-c(row_num, geometry))

merged <- pm25 %>%
  left_join(., sites, by = c("site_name", "state")) %>%
  st_set_geometry(NULL) %>%
  left_join(., noaa, by = c("station_name","date")) %>%
  select(-c(geometry, state.y)) %>%
  rename(state = state.x)
write.csv(merged, str_c(data_out, "/merged_all.csv"), row.names=FALSE)

#######################
## linear regression ##
#######################

merged_all <- read_csv(make_path(config$data_path$merge,
                   "all_w_aod.csv")) %>%
  select(-X1) %>%
  na.omit()

reg_vars <- merged_all %>%
  select(elevation, longitude, latitude, contains("normal"),
         aod_value47, aod_value55, day_of_week, weekday, season,
         aod_value47) %>%
  names() %>%
  paste(collapse = " + ")

lm_mod <- lm(as.formula(paste0("daily_mean_pm_2_5_concentration ~ ", reg_vars,
                                 "+ aod_value47:mtd_prcp_normal +
                               aod_value55:mtd_prcp_normal +
                               aod_value47:dly_tavg_normal +
                               aod_value55:dly_tavg_normal")),
   data = merged_all)

lm_mod2 <- lm(as.formula(paste0("daily_mean_pm_2_5_concentration ~ ", reg_vars,
                                " + factor(site_name)")),
              data = merged_all)
