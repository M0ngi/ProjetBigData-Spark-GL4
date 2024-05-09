FROM grafana/grafana-enterprise

USER root
RUN apk add npm

# Expose the Grafana port
EXPOSE 3000

ENV GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=grafana-mongodb-datasource

# Start Grafana
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
