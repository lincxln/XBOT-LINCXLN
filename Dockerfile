FROM lincxln/xdocker:buster

RUN mkdir /lincxln && chmod 777 /lincxln
ENV PATH="/lincxln/bin:$PATH"
WORKDIR /lincxln

RUN git clone https://github.com/lincxln/XBOT-LINCXLN -b alpha /lincxln

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/lincxln/XBOT-LINCXLN/alpha/requirements.txt

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /lincxln/

#
# Make open port TCP
#
EXPOSE 80 443

#
# Finalization
#
CMD ["python3","-m","userbot"]
