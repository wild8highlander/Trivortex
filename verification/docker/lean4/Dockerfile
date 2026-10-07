FROM ghcr.io/leanprover-community/leanprover-community:latest
WORKDIR /app
COPY lean4/ /app/lean4/
WORKDIR /app/lean4
ENTRYPOINT ["lake", "build"]
