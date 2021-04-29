FROM alfianandaa/alf:groovy

RUN mkdir /xnewbie && chmod 777 /xnewbie
ENV PATH="/xnewbie/bin:$PATH"
WORKDIR /xnewbie

RUN git clone https://github.com/lincxln/XBOT-LINCXLN -b alpha /xnewbie

#Install python requirements
RUN pip3 install -r https://raw.githubusercontent.com/lincxln/XBOT-LINCXLN/alpha/requirements.txt

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /xnewbie/

#
# Make open port TCP
#
EXPOSE 80 443

#
# Finalization
#
CMD ["python3","-m","userbot"]
