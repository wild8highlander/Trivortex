FROM coqorg/coq:8.18-ocaml-4.14
WORKDIR /app
COPY coq/ /app/coq/
WORKDIR /app/coq
RUN coq_makefile -f _CoqProject -o Makefile && make
ENTRYPOINT ["sh", "-c", "echo Coq build OK"]
