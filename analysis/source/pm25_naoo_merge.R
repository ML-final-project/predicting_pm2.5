library(yaml)
library(rprojroot)
library(tidyverse)
library(lubridate)
library(snakecase)
library(sf)
library(gganimate)

setwd("~/final_project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)
data_out <- make_path(config$data_path$merge)
source(str_c(config$group_code, "prelim.R"))

####################################
## plotting and intersecting data ##
####################################

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
write.csv(intersections, str_c(data_out, "/merged_noaa_pm25.csv"))

########################################################
## testing correlation between pm2.5 monitoring sites ##
########################################################

pm25_filtered <- pm25_avrg %>%
  filter(month == "01")

dist <- data.frame(st_distance(pm25_filtered))
site_names <- pm25_filtered$site_name
colnames(dist) <- site_names
dist_df <- dist %>%
  mutate_all(as.numeric)
dist_df <- dist_df %>%
  mutate(site_names = site_names) %>%
  select(site_names, everything())
site_names_loop <- colnames(dist_df)[2:31]

output <- list()
for (i in site_names_loop){
  df <- dist_df %>%
    filter(!!ensym(i) == 0) %>%
    select(site_names)
  output[[i]] <- df$site_names
}

pm25_avrg %>%
  filter(site_name %in% output$`4TH DISTRICT COURT`) %>%
  ggplot() +
  geom_line(aes(x = month, y = monthly_average, group = site_name))

output_df <- tibble()
for (i in site_names_loop){
  df <- pm25_avrg %>%
    st_set_geometry(NULL) %>%
    filter(site_name %in% output[[i]]) %>%
    mutate(loop = i)
  output_df <- bind_rows(output_df, df)
}

#plot_list <- list()
#for (i in site_names_loop){
#  p <- output_df %>%
#    filter(loop == i) %>%
#    ggplot() +
#    geom_line(aes(x = month, y = monthly_average, group = site_name)) +
#    labs(title = i,
#         x = "Month",
#         y = "Monthly average") +
#    theme_minimal()
#  plot_list[[i]] <- p
#}

for (i in site_names_loop) {
  output_df %>%
    filter(loop == i) %>%
    ggplot() +
    geom_line(aes(x = month, y = monthly_average, group = site_name)) +
    labs(title = i,
         x = "Month",
         y = "Monthly average") +
    theme_minimal()
#  ggsave(paste0(to_snake_case(i), ".png"), plot = last_plot(), path = out_path)
}

plot_list$`4TH DISTRICT COURT`
plot_list$`CAMP LOGAN TRAILER`
# ggsave(paste0(i, ".png"), plot = last_plot(), path = out_path)

# work on exporting the plots
