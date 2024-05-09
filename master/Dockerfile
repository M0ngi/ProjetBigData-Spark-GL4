FROM liliasfaxi/hadoop-cluster:latest

# RUN mkdir /var/run/sshd
COPY mapred-site.xml /usr/local/hadoop/etc/hadoop/mapred-site.xml

COPY entrypoint.sh /

COPY tools/ /root/

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
