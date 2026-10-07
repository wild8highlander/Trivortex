FROM makarius/isabelle:Isabelle2023
WORKDIR /app
COPY isabelle/ /app/isabelle/
WORKDIR /app/isabelle
RUN isabelle build -D .
ENTRYPOINT ["isabelle", "build", "-D", "."]
