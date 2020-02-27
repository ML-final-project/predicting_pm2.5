library(tidyverse)
library(snakecase)

setwd("~/Documents/GitHub/final_project/analysis")

noa_pm25 <- read_csv("~/Documents/GitHub/final_project/data/merged/merged_noaa_pm25.csv")
aod_imp_47 <- read_csv("~/Documents/GitHub/final_project/data/AOD/2010ImputedOpticalDepth_047nm.csv",
                       col_names = FALSE)
#aod_imp_47 %>% rename(X1 = date, X2 = aod_47mn)
names(aod_imp_47)[1] <- "date"
names(aod_imp_47)[2] <- "aod_47mn"

aod_imp_55 <- read_csv("~/Documents/GitHub/final_project/data/AOD/2010ImputedOpticalDepth_055nm.csv",
                       col_names = FALSE)
names(aod_imp_55)[1] <- "date"
names(aod_imp_55)[2] <- "aod_55mn"

df <- merge(noa_pm25,aod_imp_47, by.x = "date.x", by.y = "date")
df2 <- merge(df,aod_imp_55, by.x = "date.x", by.y = "date")




