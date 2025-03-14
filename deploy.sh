docker rm -f whu_raid-django
docker image rm whu_raid
docker build -t whu_raid .
docker run -it --network=traefik --label "traefik.enable=true" --label "traefik.http.routers.whuraid.rule=Host(\`api.whuraid.temp.ziqiang.net.cn\`)" --label "traefik.http.routers.whuraid.entrypoints=websecure" --label "traefik.http.services.whuraid.loadbalancer.server.port=8086" --name whu_raid-django whu_raid