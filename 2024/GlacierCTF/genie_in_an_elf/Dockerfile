# Ubuntu 24.04
# GCC 13.2.0
# Clang 18.0
# GLIBC 2.39

#################
# Runner system #
#################
FROM docker.io/library/ubuntu@sha256:3f85b7caad41a95462cf5b787d8a04604c8262cdcdf9a472b8c52ef83375fe15

# Install apt dependencies if needed
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y socat coreutils && apt-get install -y gdb && apt-get install -y curl && curl -LO https://github.com/pwndbg/pwndbg/releases/download/2024.08.29/pwndbg_2024.08.29_amd64.deb && apt-get install -y ./pwndbg_2024.08.29_amd64.deb && apt-get clean

# Copy challenge required files
RUN mkdir -p /app
COPY challenge /app/challenge
RUN chmod +x /app/challenge
COPY flag.txt /flag.txt
COPY entrypoint.sh /app/entrypoint.sh

CMD socat TCP-LISTEN:1337,fork,nodelay,reuseaddr,pktinfo EXEC:"/app/entrypoint.sh"
