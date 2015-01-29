# bitQuant

  - Easy tools to add trade data from exchange APIs into SQL servers - (almost)Complete
  - Backtesting structure for testing trade scripts agaisnt SQL data - Planning
  - Live trading via exchange APIs and trade scripts - Not yet

##Purpose
The goal of bitQuant is to provide a complete package for gathering Bitcoin trade data and implementing algorithmic trading. Anyone with a MySQL server and a bit of python knowledge will be able to easily gather live data, build a library, perform backtesting on their trade data, and bring the algorithms live.

**Current Features**
- Pull live trade history data from exchange APIs
- Store data on MySQL server
- Convert trade data into price history for any period
- Retrieve MySQL data as easy to use pandas DataFrames
- Quandl API support (end of day price history)

**Planned Features**
- Server scripts for automatic exchange pings and data maintence
- Complete wiki on all modules
- Backtesting strategies MySQL data utilizing bt (https://github.com/pmorissette/bt)
- Indicators built for use with pandas
- Machine learning tools
- Live algorithmic trading setup
