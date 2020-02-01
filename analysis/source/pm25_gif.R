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
                           "pm25_illinois_2010.csv")) %>%
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

anim_save("pm25_plot.gif", animation = last_animation(), path = out_path)
