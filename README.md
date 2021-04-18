# python-code

This repository has python code with some useful utilities

**1. autoretweet:** This Code will retweet tweets from particular handle or with particular hashtags. You need to generate your tokens from https://developer.twitter.com and then place it in settings.py

You can schedule this program in cron and run it as a twitter bot which will automatically RT tweets with mentioned hashtags or from handle.

Note: Keep in mind every social media platform has some restrictions(twitter too), please go through documentation about how many tweet or retweets you can do in particular time.

For more info you can visit https://developer.twitter.com/

**2. quotegenerator:** This program will take two parameters as input and will create image out of it. You can use this to automate your social media posts.

Modify settings.py for Font file, Output Storage and Background Image path

Run: python generateInsta.py "outputfile" "Text to Print on the background image"

TODO: Background Image size is hardcoded(1080x1080), need to parameterize it
