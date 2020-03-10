library(yaml)
library(rprojroot)
library(tidyverse)
library(lubridate)
library(sf)
library(gganimate)
library(snakecase)
library(transformr)
library(gapminder)

setwd("~/final_project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)

pm25 <- read_csv(make_path(config$data_path$pm25,
                           "pm25_illinois.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  mutate(date = mdy(date))

illinois_shape <- st_read(
  make_path(config$data_path$shape, "tl_2016_17_cousub.shp")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  rename(county_code = countyfp)

p <- ggplot() +
  geom_sf(data = illinois_shape) +
  geom_point(data = pm25,
             aes(x = site_longitude,
                 y = site_latitude,
                 size = daily_mean_pm_2_5_concentration,
                 color = site_name)) +
  transition_components(date) +
  labs(title = 'Daily PM2.5 Concentrations (2010)',
       subtitle = '{frame_time}') +
  theme(
    legend.position="none",
    line = element_blank(),
    rect = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank(),
    panel.grid.major = element_line(colour = "transparent")
  )
animate(p, renderer = gifski_renderer(
  file = NULL, loop = TRUE, width = NULL, height = NULL),
  duration = 20)

#anim_save("pm25_plot.gif", animation = last_animation(), path = out_path)

####################
## plotting merge ##
####################

chicago_shape <- st_read(
  make_path(config$data_path$shape,
            "geo_export_bae420c7-e252-4c44-920c-53c667dbb756.shp")) %>%
  set_names(to_snake_case(colnames(.)))

noaa_plotting <- read_csv(make_path(config$data_path$noaa,
                                    "Chicago2010Daily.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  select(station_name, longitude, latitude) %>%
  na.omit() %>%
  st_as_sf(coords = c("longitude", "latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform(2163)

pm25_plotting <- read_csv(make_path(config$data_path$pm25,
                                     "pm25_chicago_2010.csv")) %>%
  set_names(to_snake_case(colnames(.))) %>%
  st_as_sf(coords = c("site_longitude", "site_latitude"),
           crs = 4326, remove = FALSE) %>%
  select(site_name, site_longitude, site_latitude) %>%
  st_transform(2163)

pm25_sites <- distinct(pm25_plotting, site_name)
noaa_sites <- distinct(noaa_plotting, station_name)

min.col <- function(m, ...) max.col(-m, ...)
pm25_sites$row_num <- st_distance(pm25_sites, noaa_sites) %>% min.col(.)

sites <- noaa_sites %>%
  mutate(row_num = row_number()) %>%
  st_set_geometry(NULL) %>%
  right_join(., pm25_sites, by = "row_num") %>%
  select(-c(row_num, geometry))

noaa_plotting_null <- noaa_plotting %>%
  st_set_geometry(NULL) %>%
  distinct()

merge_plot <- pm25_plotting %>%
  left_join(., sites, by = "site_name") %>%
  st_set_geometry(NULL) %>%
  distinct() %>%
  left_join(., noaa_plotting_null, by = "station_name")

pm25_plot <- merge_plot %>%
  select(site_name, site_longitude, site_latitude) %>%
  st_as_sf(coords = c("site_longitude", "site_latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=longlat +ellps=WGS84 +no_defs")

noaa_plot <- merge_plot %>%
  select(station_name, longitude, latitude) %>%
  st_as_sf(coords = c("longitude", "latitude"),
           crs = 4326, remove = FALSE) %>%
  st_transform("+proj=longlat +ellps=WGS84 +no_defs")

n <- 14
qual_col_pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
col_vector <- unlist(mapply(
  brewer.pal, qual_col_pals$maxcolors, rownames(qual_col_pals)))

ggplot() +
#  geom_sf(data = chicago_shape) +
  geom_sf(data = pm25_plot) +
  geom_sf(data = noaa_plot, aes(color = sample(col_vector, n)))
