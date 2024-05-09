#!/bin/bash


echo "Starting proxy server"
sleep 10

chown grafana:root /var/lib/grafana -R

cd /var/lib/grafana/plugins/mongodb-grafana
npm i --force
npm run server &

cd /

echo "Starting grafana server"
sleep 10

ls -la /var/lib/

su grafana -s /bin/bash -c "grafana-server --config=/etc/grafana/grafana.ini --homepath=/usr/share/grafana"
