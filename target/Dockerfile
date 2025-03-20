FROM alpine:3.21.3

RUN apk add --no-cache openssh openrc

RUN mkdir /etc/openrc
RUN touch /etc/openrc/softlevel

RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh && \
    touch /root/.ssh/authorized_keys && \
    chmod 600 /root/.ssh/authorized_keys && \
    ssh-keygen -A && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "Port 2222" >> /etc/ssh/sshd_config

RUN echo "root:xxxxxxxx" | chpasswd

RUN rc-update add sshd

EXPOSE 2222

WORKDIR /root

CMD ["/sbin/init", "noautdetect"]
