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

####################
## plotting merge ##
####################

noaa_plotting <- noaa %>%
  select(station_name, longitude, latitude) %>%
  st_set_geometry(NULL) %>%
  distinct()

merge_plotting <- pm25 %>%
  left_join(., sites, by = "site_name") %>%
  left_join(., noaa_plotting, by = "station_name") %>%
  st_transform(4326) %>%
  distinct(site_name, station_name, longitude, latitude)

ggplot(merge_plotting) +
  geom_sf() +
  geom_point(aes(x = longitude, y = latitude), color = "red")

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

################################################
## adding lags and seasons/weekday indicators ##
################################################

lagmatrix <- function(x,max.lag) embed(c(rep(NA,max.lag), x), max.lag+1)
lag_prcp <- data.frame(lagmatrix(merged_aod$mtd_prcp_normal, 1)) %>%
  select(X2) %>%
  rename(mtd_prcp_normal_lag1 = X2)
lag_snow <- data.frame(lagmatrix(merged_aod$mtd_snow_normal, 1)) %>%
  select(X2) %>%
  rename(mtd_snow_normal_lag1 = X2)
merge_lag <- cbind(merged_aod, lag_prcp, lag_snow)

#######################
## linear regression ##
#######################

reg_vars <- merge_lag %>%
  select(elevation, contains("normal"), aod47, aod55) %>%
  names() %>%
  paste(collapse = " + ")

summary(plm(as.formula(paste0("daily_mean_pm_2_5_concentration ~ ", reg_vars)),
            data = merge_lag,
            index = c("date"),
            model = "pooling",
            effect = "twoways"))

# for markdown
# library(stargazer)
# stargazer(merge_lag)
