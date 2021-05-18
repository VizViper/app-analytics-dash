# Background
* On a daily basis, the relative rankings of mobile applications are compiled by the major app stores (i.e. Apple and Android), and are chiefly categorized by (1) grossing - the overall revenue that passes through the app store, and (2) downloads - the number of times an application has been downloaded from the app store.
* These rankings are indicative of relative revenue performance and audience growth, and when the daily rankings are compiled in a time series, can be illustrative of revenue and downloads trends across a specified time period.

### Example of daily app rankings from [AppAnnie](https://www.appannie.com/en/)

![image](https://user-images.githubusercontent.com/69601778/118708192-472acd00-b7d0-11eb-9d07-c7bbf4fb0e09.png)

* Building upon our previous ETL project, which established a process for dynamically scraping the daily app rankings for the top-300 U.S. applications on both Apple and Android, we sought to write a program that can feed this data to a web page optimized for visualizing trends on a publisher-specific basis.

# Key Milestones / Project Outline
  * Gather daily historical data on mobile applications from major app stores (i.e. Apple and Android) via scraping the website AppAnnie, using Splinter and Beautiful Soup
  * Store scraped data in local SQL database using Pandas, SQLAlchemy, and pgAdmin
  * Clean historical rankings data from existing Excel file using VBA and Pandas
  * Merge scraped data and historical data in local SQL database using Postgres, Pandas, and SQLAlchemy
JSONify the data from the SQL database
  * Use Flask to serve the JSONified data to an HTML page built with Bootstrap
  * Use Javascript to filter data for platform (iOS and Android) and publisher, based on drop-down menus
  * Use Javascript, D3, and Upper Deck to visualize ranking trends across a selected publisher’s catalog of apps on a timeseries chart

![image](https://user-images.githubusercontent.com/69601778/118709720-324f3900-b7d2-11eb-8c90-bfc55cce1864.png)


  * Use Javascript and D3 to create dynamic summary table based on drop-down parameters


