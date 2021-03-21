# tesla-bmaas

docker create --name tesla-bmaas -e TOKEN="github-personal-access-token-for-runner-token" -e REPO="oizone/tesla-bmaas" -e RUNNER_NAME="bmaas-runner" -e RUNNER_LABELS="lab" -p 80:80 oizone/tesla-bmaas