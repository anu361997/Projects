#we upload data from local folder
covid19 = read.csv("/home/anamika/Desktop/Books_SEM_2/AI/AI Term Paper/covid19-main_india/covid19-main/WHO_dataset/time-series-19-covid-combined.csv")

# choose variables to import as Time Series, in this case we are interested only 
#in data from France, we use ts for Time Series of new cases and new deaths statistics
covid19_F=covid19[covid19$Country=="India"]
covid19_F_nc=ts(covid19_F$Confirmed)
covid19_F_nd=ts(covid19_F$Deaths)
s
# library forecast permits us using many functions that are essential for time series forecasting
library(forecast)

#we plot data to see what we shall work with, to get an idea if data has trend or seasonality 
autoplot(covid19_F_nd)+ ggtitle('Number of new deaths of Covid19 in India')+ xlab('days')+ ylab('Number of deaths of Covid19')
library(ggplot2) 
autoplot(covid19_F_nc) +
  ggtitle('Number of new cases of Covid19 in India')+ 
  xlab('days')+ ylab('Number of new cases of Covid19')

# we use auto-correlation function to see if data has significant patterns
acf(covid19_F_nc)

#we set frequency to 7 as data has been gathered daily, so we devide it into weekly periods
covid19_F_nc=ts(covid19_F_nc,freq=7) 

#we perform data lagging
acf(diff(covid19_F_nc,lag=7))

#using halt-winters model we try to fit data and plot the results
fit=hw(covid19_F_nc) 
autoplot(forecast(fit,h=7))

# we display our forecast
print(forecast(fit,h=7))

#we plot our forecasted model on real data
prev=forecast(fit,h=7)
autoplot(prev) + autolayer(tail(covid19_F_2_nc,7), series="true data")+
  autolayer(prev$mean, series="HW forecasts")


autoplot(tail(covid19_F_2_nc,17*7), 
         series="true data")+ autolayer(prev$mean, series="HW forecasts")

# results turn out to be not bad :) indeed not exactly close to reality. 
#We could see forecast line allign the real data, but having a lower amplitude 

