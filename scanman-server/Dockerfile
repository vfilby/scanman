FROM phusion/baseimage:bionic-1.0.0

ENV WAIT_ON_TRANSFER_TOKEN=false
ENV SETTLE_DURATION=5
ENV ENABLE_SSH_SERVER=true
ENV INTAKE_DIR=/scanman/intake
ENV COMPLETED_DIR=/scanman/completed

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# SSHD Config
#
RUN rm -f /etc/service/sshd/down

# Regenerate SSH host keys. baseimage-docker does not contain any, so you
# have to do that yourself. You may also comment out this instruction; the
# init system will auto-generate one during boot.
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
ADD config/my_init.d/set_authorized_ssh_keys.sh /etc/my_init.d/set_authorized_ssh_keys.sh
RUN chmod +x /etc/my_init.d/set_authorized_ssh_keys.sh

# ScanMan Config
#
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y --no-install-recommends \
  python3 \
  python3-venv \
  python3-setuptools \
  python3-pip \
  libyaml-dev \
  netpbm \
  ghostscript \
  poppler-utils \
  imagemagick \
  unpaper \
  util-linux \
  tesseract-ocr \
  parallel \
  units \
  ssh \
  git \
  vim \
  bc


# # RUN git clone --branch dir-option https://github.com/vfilby/sane-scan-pdf.git

#
#
# COPY test-data test-data
WORKDIR /scanman
COPY app/* /scanman/
#COPY Pipfile* /scanman/
COPY .build/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN chmod +x scanman.py

RUN mkdir -p /scanman/intake
RUN mkdir -p /scanman/completed

# Docker/Python Version/Venv dance
# See: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/

#ENV VIRTUAL_ENV=/opt/venv
#RUN python3 -m venv $VIRTUAL_ENV
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#RUN pipenv install


RUN mkdir -p /etc/service/scanman
COPY config/scanman_run /etc/service/scanman/run
RUN chmod +x /etc/service/scanman/run




# RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
#
# ADD run.sh /run.sh

# RUN chmod +x /*.sh

#RUN mkdir -p /var/run/sshd && sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config \
#  && sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
#  && touch /root/.Xauthority \
#  && true





#
#
#

# VOLUME ['/scanman/dropbox','/scanman/completed']
#
#
# EXPOSE 22
