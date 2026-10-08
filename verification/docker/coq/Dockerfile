FROM coqorg/coq:8.18-ocaml-4.14
# TRIVORTEX verification — pinned Coq/Rocq toolchain (milestone M1)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
USER root
WORKDIR /app
COPY coq/ /app/coq/
WORKDIR /app/coq
# the CI-callable check of the M1 acceptance criteria: the statement layer
# compiles and Print Assumptions reports the closed axiom footprint
RUN coqc Trivortex.v && rm -f Trivortex.vo Trivortex.vos Trivortex.vok Trivortex.glob .Trivortex.aux
ENTRYPOINT ["sh", "-c", "coqc Trivortex.v && echo 'Coq build OK — statement layer verified'"]
