FROM fme-desktop-base:latest

ADD bin/entrypoint.sh /bin/entrypoint

RUN chmod +x bin/entrypoint

WORKDIR /opt/fme-desktop-${FME_MAJOR}
ENV PATH="/opt/fme-desktop-${FME_MAJOR}:${PATH}"

ENTRYPOINT ["entrypoint"]
CMD ["fme", "-v"]
