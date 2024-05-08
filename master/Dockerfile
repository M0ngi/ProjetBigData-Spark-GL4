FROM liliasfaxi/hadoop-cluster:latest

# RUN mkdir /var/run/sshd
COPY mapred-site.xml /usr/local/hadoop/etc/hadoop/mapred-site.xml

COPY entrypoint.sh /

COPY kafka_stream_handler.py /root/kafka_stream_handler.py

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
