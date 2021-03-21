FROM mcr.microsoft.com/dotnet/sdk:latest
LABEL maintainer="oizone@oizone.net"

ARG GH_RUNNER_VERSION="2.274.2"
ARG TARGETPLATFORM

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV ANSIBLE_HOST_KEY_CHECKING=False
ARG APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=yes

#RUN dpkg -i packages-microsoft-prod.deb
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 unzip xorriso python3-boto3 jq nginx gnupg2 python3-openpyxl p7zip-full
RUN echo deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main | tee -a /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
RUN apt-get update
RUN apt-get install -y --no-install-recommends ansible
RUN ln -sf /iso /var/www/iso


RUN mkdir /httpboot
RUN mkdir /iso

COPY create-hosts.py /httpboot/
COPY nginx.conf /httpboot/

RUN ln -sf /httpboot/nginx.conf /etc/nginx/sites-enabled/default

WORKDIR /actions-runner
COPY install_actions.sh /actions-runner

RUN chmod +x /actions-runner/install_actions.sh \
  && /actions-runner/install_actions.sh ${GH_RUNNER_VERSION} ${TARGETPLATFORM} \
  && rm /actions-runner/install_actions.sh

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
