#!/bin/bash -x
#GH_RUNNER_VERSION=$1
GH_RUNNER_VERSION=`curl -s https://api.github.com/repos/actions/runner/releases/latest|grep tag_name|cut -d"\"" -f 4|sed 's/v//'`
TARGETPLATFORM=$2

export TARGET_ARCH="x64"
if [[ $TARGETPLATFORM == "linux/arm/v7" ]]; then
  export TARGET_ARCH="arm"
elif [[ $TARGETPLATFORM == "linux/arm64" ]]; then
  export TARGET_ARCH="arm64"
fi

curl -L "https://github.com/actions/runner/releases/download/v${GH_RUNNER_VERSION}/actions-runner-linux-${TARGET_ARCH}-${GH_RUNNER_VERSION}.tar.gz" > actions.tar.gz
tar -zxf actions.tar.gz
rm -f actions.tar.gz
#./bin/installdependencies.sh
mkdir /_work
