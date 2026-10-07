FROM haskell:9.4-slim
WORKDIR /app
COPY haskell/ /app/haskell/
WORKDIR /app/haskell
RUN cabal update && cabal build all
ENTRYPOINT ["sh", "-c", "for s in section1_correctionb section2_preprintnse section3_abcloud section4_kdv section5_kleinattractor section6_riemannzeros; do cabal run verify_$s; done"]
