# ServDeal structure

`web/` and `mobile/` are separate frontends. Both call the FastAPI service in `api/` and use the dedicated ServDeal Supabase project.

The current API is a small functional starter. Before adding vendor authentication or payments, split each endpoint into `routes/`, `schemas/`, `repositories/`, and `services/` modules following the AIMates pattern.
