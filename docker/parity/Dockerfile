FROM parity/parity

COPY docker/parity/start.sh /opt/parity/start.sh
COPY docker/parity/ecip1017chain.json /opt/parity/ecip1017chain.json

RUN chmod +x /opt/parity/start.sh

EXPOSE 8080 8555 8180
EXPOSE 30303
EXPOSE 30303/udp

WORKDIR /opt/parity

CMD ["/opt/parity/start.sh"]
