FROM liliasfaxi/hadoop-cluster:latest

# RUN mkdir /var/run/sshd

COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
