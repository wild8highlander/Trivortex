FROM agda/agda:2.6.4
# TRIVORTEX verification — pinned Agda toolchain (milestone M2)
# SPDX-FileCopyrightText: 2026 Isaev Iskhak Khamzatovich
# SPDX-License-Identifier: LicenseRef-Proprietary-Wild8Highlander-1.0
USER root
WORKDIR /app
COPY agda/ /app/agda/
WORKDIR /app/agda
# the CI-callable check of the M2 acceptance criteria: the constructive
# angle-arithmetic module type-checks (stdlib ships inside the image)
RUN agda Trivortex.agda && rm -f Trivortex.agdai _build/*
ENTRYPOINT ["sh", "-c", "agda Trivortex.agda && echo 'Agda check OK — constructive module verified'"]
