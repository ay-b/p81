FROM ubuntu:22.04

# TODO Reduce RUN layers

RUN apt update && apt upgrade -y &&\
    DEBIAN_FRONTEND=noninteractive apt install curl gnupg2 git unzip jq wget -y

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" &&\
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

RUN wget -q -O - https://api.github.com/repos/weaveworks/eksctl/releases \
    | jq --raw-output 'map( select(.prerelease==false) | .assets[].browser_download_url ) | .[]' \
    | grep inux \
    | head -n 1 \
    | wget -q --show-progress -i - -O - \
    | tar -xz -C /usr/local/bin

RUN wget -q https://github.com/mikefarah/yq/releases/download/3.4.1/yq_linux_amd64 -O yq && \
    chmod +x yq

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash - 


RUN curl https://releases.hashicorp.com/terraform/1.4.5/terraform_1.4.5_linux_amd64.zip -o tf.zip &&\
    unzip tf.zip &&\
    rm tf.zip &&\
    mv terraform /usr/local/bin/

RUN curl  https://releases.hashicorp.com/packer/1.8.6/packer_1.8.6_linux_amd64.zip -o packer.zip &&\
    unzip packer.zip &&\
    rm packer.zip &&\
    mv packer /usr/local/bin/

# TODO Clean up all the mess after installation to make image smaller

CMD /usr/bin/bash
