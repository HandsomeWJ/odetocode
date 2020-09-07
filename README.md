# OdeToCode

## Telegram Bot User Guide

Telegram Bot ID: [@risk_tolerance_test_bot](https://t.me/risk_tolerance_test_bot)  
Webpage deployed on Elastic Beanstalk: http://deploy.eba-tcb5tsyy.us-west-2.elasticbeanstalk.com

### Instructions:
- Add our telegram bot by user ID: risk_tolerance_test_bot
- Start conversation with our telegram bot and answer the questions accordingly.
- Receive final score and enter it in the [Investing For Youth](http://deploy.eba-tcb5tsyy.us-west-2.elasticbeanstalk.com/risk.html) website.

> Due to time limit, currently our Telegram Bot is hosted locally. We can simply run it locally by running command "python3 MyBot.py". Our final product is a minimum viable product.
If given more time, we are planning to run it on AWS EC2.

## Website User Guide

Excluding the home page, there are three main pages.

- [Risk Analysis](http://deploy.eba-tcb5tsyy.us-west-2.elasticbeanstalk.com/risk.html) takes the score obtained from the Telegram Bot and generates an optimal complete portfolio using the Markowitz Portfolio Theory. User will be asked to allocate a portion of their total capital into the portfolio, and the remaining into a risk-free asset (10Y Singapore Government Bond)
- [Beginner's Guide](http://deploy.eba-tcb5tsyy.us-west-2.elasticbeanstalk.com/guide.html) provides a list of news articles for the novice investor to take their first step into the world of investing.
- [Financial News](http://deploy.eba-tcb5tsyy.us-west-2.elasticbeanstalk.com/news.html) provides a list of news articles pertaining to financial information about the market, as well as the stocks in your portfolio. These news articles are dynamically generated using the [Finnhub API](https://finnhub.io/). 