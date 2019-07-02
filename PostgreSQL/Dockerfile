FROM postgres:11
MAINTAINER Sam Mosleh <sam.mosleh@ut.ac.ir>

RUN mkdir backup \
  && cd backup \
  && touch cron_file \
  && echo "01 00 * * * pg_dump --username postgres > ./postgres.bak" >> cron_file \
  && crontab cron_file && rm cron_file
