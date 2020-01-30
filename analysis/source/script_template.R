library(yaml)
library(rprojroot)
library(tidyverse)

setwd("~/ML-final-project/")

make_path <- is_git_root$make_fix_file()
config <- yaml.load_file(make_path("analysis/config.yml"))
out_path <- make_path(config$build_path)

pm25 <- read_csv(make_path(config$data_path$pm25, "pm25_chicago_2010.csv"))

# exporting plots/graphs
# ggsave(str_c(out_path, "/plot_name.png"))
