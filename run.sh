set -e
app="api_proxy"

docker build -t ${app} .

docker run -p 8080:8080 ${app}
