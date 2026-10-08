FROM makarius/isabelle:Isabelle2024
# TRIVORTEX verification — pinned Isabelle/HOL toolchain (milestone M2)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
WORKDIR /app
COPY isabelle/ /app/isabelle/
WORKDIR /app/isabelle
# the CI-callable check of the M2 acceptance criteria: the HOL session
# builds (the optional SMT session stays disabled until Z3 is installed)
RUN isabelle build -D .
ENTRYPOINT ["isabelle", "build", "-D", "."]
